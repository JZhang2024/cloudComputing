'''lambda function to upload metadata of s3 object to dynamodb table'''
import urllib.parse
import boto3

print('Loading function')
s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb', region_name='us-east-1')


def lambda_handler(event, context):
    '''lambda function to upload metadata of s3 object to dynamodb table'''
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
        #retrieve s3 object ARN from s3 object
        arn = f'arn:aws:s3:::{bucket}/{key}'
        #retrieve entity tag from s3 object
        etag = response['ETag']
        #write metadata to dynamodb table with primary key as file_name
        item = {
            'file_name': {'S': key},
            'file_size': {'S': size_with_unit},  # Store the size with unit
            'upload_date': {'S': str(last_modified)},
            'file_ARN': {'S': arn},
            'eTag': {'S': etag}
        }
        dynamo.put_item(TableName='hw05-table', Item=item)
        #return response['ContentType']
    except Exception as bucket_exception:
        print(bucket_exception)
        print(f'Error getting object {key} from bucket {bucket}')
        raise bucket_exception
