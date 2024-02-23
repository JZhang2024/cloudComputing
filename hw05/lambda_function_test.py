'''tests for lambda function to upload metadata of s3 object to dynamodb table'''
import boto3
from moto import mock_aws
from upload_lambda_function import lambda_handler
from delete_lambda_function import delete_lambda_handler

@mock_aws
def test_upload_lambda_handler():
    '''test for lambda function to upload metadata of s3 object to dynamodb table'''
    # Set up mock S3
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_client.create_bucket(Bucket='test-bucket')
    s3_client.put_object(Bucket='test-bucket', Key='test-key', Body='test-content')

    # Set up mock DynamoDB
    dynamo = boto3.client('dynamodb', region_name='us-east-1')
    dynamo.create_table(
        TableName='hw05-table',
        KeySchema=[{'AttributeName': 'file_name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'file_name', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    # Create mock event
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'test-bucket'
                    },
                    'object': {
                        'key': 'test-key'
                    }
                }
            }
        ]
    }

    # Call the lambda handler
    lambda_handler(event, None)

    # Check that the item was added to DynamoDB
    response = dynamo.get_item(TableName='hw05-table', Key={'file_name': {'S': 'test-key'}})
    assert 'Item' in response
    assert response['Item']['file_name']['S'] == 'test-key'
    assert response['Item']['file_size']['S'] == '12 bytes'  # Length of 'test-content'
    assert response['Item']['file_ARN']['S'] == 'arn:aws:s3:::test-bucket/test-key'

@mock_aws
def test_upload_lambda_handler_folder_of_objects():
    '''test for lambda function when multiple objects are uploaded to s3 bucket
    lambda is automatically called individually for each object in the folder,
    so only first object of event is processed'''
    # Set up mock S3
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_client.create_bucket(Bucket='test-bucket')
    s3_client.put_object(Bucket='test-bucket', Key='test-folder/test-key1', Body='test-content')
    s3_client.put_object(Bucket='test-bucket', Key='test-folder/test-key2', Body='test-content')

    # Set up mock DynamoDB
    dynamo = boto3.client('dynamodb', region_name='us-east-1')

    dynamo.create_table(
        TableName='hw05-table',
        KeySchema=[{'AttributeName': 'file_name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'file_name', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    # Create mock event
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'test-bucket'
                    },
                    'object': {
                        'key': 'test-folder/test-key1'
                    }
                }
            },
            {
                's3': {
                    'bucket': {
                        'name': 'test-bucket'
                    },
                    'object': {
                        'key': 'test-folder/test-key2'
                    }
                }
            }
        ]
    }

    # Call the lambda handler
    lambda_handler(event, None)

    # Check that the items were added to DynamoDB
    response = dynamo.get_item(TableName='hw05-table',
                               Key={'file_name': {'S': 'test-folder/test-key1'}})
    assert 'Item' in response
    assert response['Item']['file_name']['S'] == 'test-folder/test-key1'
    assert response['Item']['file_size']['S'] == '12 bytes'
    assert response['Item']['file_ARN']['S'] == 'arn:aws:s3:::test-bucket/test-folder/test-key1'

    response = dynamo.get_item(TableName='hw05-table',
                               Key={'file_name': {'S': 'test-folder/test-key2'}})
    # Second object should not be in DynamoDB because real events would be processed individually
    assert 'Item' not in response

@mock_aws
def test_delete_lambda_handler():
    '''test for delete_lambda_handler
    that creates a csv file with the list of files in the s3 bucket'''
    # Set up mock S3
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_client.create_bucket(Bucket='test-bucket')
    s3_client.put_object(Bucket='test-bucket', Key='test-key', Body='test-content')

    # Create mock event
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'test-bucket'
                    },
                    'object': {
                        'key': 'test-key'
                    }
                }
            }
        ]
    }

    # Call the lambda handler
    delete_lambda_handler(event, None)

    # Check that the csv file was added to S3 and contains the expected content
    #last modified and eTag are not tested because they are not preset in the mock s3 object
    response = s3_client.get_object(Bucket='test-bucket', Key='file_list.csv')
    response_body = response['Body'].read().decode('utf-8')
    assert 'test-key' in response_body
    assert '12 bytes' in response_body
    assert 'test-key' in response_body
