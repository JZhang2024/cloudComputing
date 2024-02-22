import pytest
import boto3
from moto import mock_aws
from upload_lambda_function import lambda_handler

@mock_aws
def test_lambda_handler():
    # Set up mock S3
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='test-bucket')
    s3.put_object(Bucket='test-bucket', Key='test-key', Body='test-content')

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