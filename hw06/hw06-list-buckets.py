import json
import boto3

'''lambda function to list all the buckets in the AWS account'''


def list_buckets_lambda_handler(event, context):
    '''lambda function to list all the buckets in the AWS account'''
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()
    #output for cloudwatch log
    account_id = event['context']['account-id']
    print(f'Listing all buckets in the AWS account {account_id}')
    bucket_names = []
    if buckets.get('Buckets') is not None:
        for bucket in buckets['Buckets']:
            bucket_names.append(bucket["Name"])
            print(f'{bucket["Name"]}')
    else:
        print('No buckets found')

    response = {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps({'buckets': bucket_names})
    }
    return response
