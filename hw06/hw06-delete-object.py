'''lambda function to delete an object from a bucket'''

import json
import boto3

def delete_object_lambda_handler(event, context):
    '''Delete object from the given bucketname. The object name
    is passed in the "body" of the post request'''

    # Get the bucketname and the object name from the request
    print(event) #log the event
    bucketname = json.loads(event['body-json'])['bucketname']
    objectname = json.loads(event['body-json'])['objectname']

    print(f'Deleting object {objectname} from bucket {bucketname}')

    # Create a new s3 client
    s3_client = boto3.client('s3')

    #if object or bucket does not exist, return 404
    try:
        s3_client.head_object(Bucket=bucketname, Key=objectname)
    except:
        print(f'Object {objectname} not found in bucket {bucketname}')
        return {
            'statusCode': 404,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': f'Object {objectname} not found in bucket {bucketname}'})
        }

    # Delete the object from the bucket
    s3_client.delete_object(Bucket=bucketname, Key=objectname)

    #confirm deletion
    try:
        s3_client.head_object(Bucket=bucketname, Key=objectname)
    except:
        print(f'Successfully deleted object {objectname} from bucket {bucketname}')
    else:
        print(f'Failed to delete object {objectname} from bucket {bucketname}')
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': f'Failed to delete object {objectname} from bucket {bucketname}'})
        }

    print(f'Successfully deleted object {objectname} from bucket {bucketname}')

    # Return the response
    response = {
        'bucketname': bucketname,
        'objectname': objectname
    }
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(response)
    }
