'''lambda function for listing all the objects in a bucket'''

import json
import boto3

def list_objects_lambda_handler(event, context):
    '''lambda function for listing all the objects in a bucket'''
    s3 = boto3.client('s3')
    response = s3.list_objects(Bucket=event['bucket'])
    #output for cloudwatch log
    if response.get('Contents') is not None:
        for obj in response['Contents']:
            print(f'{obj["Key"]}')
    else:
        print('No objects found')
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }