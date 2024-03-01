'''lambda function to list all the buckets in the AWS account'''

import json
import boto3

def list_buckets_lambda_handler(event, context):
    '''lambda function to list all the buckets in the AWS account'''
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    #output for cloudwatch log
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    print(f'Listing all buckets in the AWS account {account_id}')
    if response.get('Buckets') is not None:
        for bucket in response['Buckets']:
            print(f'{bucket["Name"]}')
    else:
        print('No buckets found')
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(response)
    }
