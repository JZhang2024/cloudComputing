'''lambda function to list all the buckets in the AWS account'''

import json
import boto3

def list_buckets_lambda_handler(event, context):
    '''lambda function to list all the buckets in the AWS account'''
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    #output for cloudwatch log
    if response.get('Buckets') is not None:
        for bucket in response['Buckets']:
            print(f'{bucket["Name"]}')
    else:
        print('No buckets found')
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }