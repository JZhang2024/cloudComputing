import json
import boto3

'''lambda function for listing all the objects in a bucket'''

def list_objects_lambda_handler(event, context):
    '''lambda function for listing all the objects in a bucket'''
    s3_client = boto3.client('s3')

    # Get the bucket-name from the request
    bucketname = event['params']['path']['bucket-name']

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
