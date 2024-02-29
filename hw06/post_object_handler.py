'''lambda function to add an object to a bucket'''

import json
import boto3

def list_buckets_lambda_handler(event, context):
    '''Add object to the given bucketname. The object file name
    and the file contents are passed in the "body" of the post request'''

    # Get the bucketname and the object name from the request
    body = json.loads(event['body'])
    bucketname = body['bucketname']
    objectname = body['objectname']
    objectcontent = body['objectcontent']

    # Create a new s3 client
    s3_client = boto3.client('s3')

    # Add the object to the bucket
    s3_client.put_object(Bucket=bucketname, Key=objectname, Body=objectcontent)

    print(f'Added object {objectname} to bucket {bucketname}')

    # Return the response
    response = {
        'bucketname': bucketname,
        'objectname': objectname,
        'objectcontent': objectcontent
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
