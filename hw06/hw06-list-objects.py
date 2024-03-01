import json
import boto3

'''lambda function for listing all the objects in a bucket'''

def list_objects_lambda_handler(event, context):
    '''lambda function for listing all the objects in a bucket'''
    s3_client = boto3.client('s3')

    # Get the bucketname from the request
    bucketname = event['bucketname']

    print(f'Listing objects in bucket: {bucketname}')
    response = s3_client.list_objects(Bucket=bucketname)
    object_names = []
    if response.get('Contents') is not None:
        for obj in response['Contents']:
            object_names.append(obj["Key"])
            print(f'{obj["Key"]}')
    else:
        print('No objects found')
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({'objects': object_names})
    }
