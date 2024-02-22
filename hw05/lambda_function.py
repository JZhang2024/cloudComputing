import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #retrieve file size from s3 object
        size = response['ContentLength']
        size_with_unit = str(size) + ' bytes'  # Specify the unit of file size
        
        #retrieve upload date from s3 object
        last_modified = response['LastModified']
        #retrieve file ARN from s3 object
        arn = response['ResponseMetadata']['HTTPHeaders']['x-amz-request-id']
        #retrieve entity tag from s3 object
        etag = response['ETag']
        
        #write metadata to dynamodb table with primary key as file_name
        item = {
            'file_name': {'S': key},
            'size': {'S': size_with_unit},  # Store the size with unit
            'last_modified': {'S': str(last_modified)},
            'arn': {'S': arn},
            'etag': {'S': etag}
        }
        
        dynamo.put_item(TableName='hw05-table', Item=item)
        #return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
