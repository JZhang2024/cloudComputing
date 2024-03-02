'''lambda function to add an object to a bucket'''

import json
import boto3
import base64

def add_object_lambda_handler(event, context):
    '''Add object to the given bucketname. The object file name
    and the file contents are passed in the "body" of the post request'''

    # Get the bucketname and the object name from the request
    bucketname = event['params']['path']['bucket-name']
    objectname = json.loads(event['body-json'])['objectname']
    objectcontent = json.loads(base64.b64decode(event['body-json']['body']))

    print(f'Adding object {objectname} to bucket {bucketname}')

    # Create a new s3 client
    s3_client = boto3.client('s3')

    #if bucket does not exist, return 404
    try:
        s3_client.head_bucket(Bucket=bucketname)
    except:
        print(f'Bucket {bucketname} not found')
        return {
            'statusCode': 404,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': f'Bucket {bucketname} not found'})
        }

    # Add the object to the bucket
    s3_client.put_object(Bucket=bucketname, Key=objectname, Body=objectcontent)

    print(f'Successfully added object {objectname} to bucket {bucketname}')

    # Return the response
    response = {
        'bucketname': bucketname,
        'objectname': objectname,
        'objectcontent': objectcontent
    }
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(response)
    }
