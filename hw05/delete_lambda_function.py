'''This lambda function is triggered when an object is deleted from the s3 bucket.'''
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb', region_name='us-east-1')

def delete_lambda_handler(event, context):
    '''When an object is deleted from the s3 bucket, the lambda will create an CSV file containing
    a list of the files currently in your S3 bucket and writes the csv file to the same S3 bucket'''

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.list_objects_v2(Bucket=bucket)
        #retrieve the list of files in the s3 bucket
        file_list = response['Contents']
        #create a csv file with the list of files in the s3 bucket
        csv_data = '\n'.join(file['Key'] for file in file_list)
        #upload the csv data to the s3 bucket
        s3.put_object(Body=csv_data, Bucket=bucket, Key='file_list.csv')

    except Exception as delete_exception:
        print(delete_exception)
        print(f'Error getting object {key} from bucket {bucket}')
        raise delete_exception
