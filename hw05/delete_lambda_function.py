import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    '''When an object is deleted from the s3 bucket, 
    the lambda will create an CSV file containing
    a list of the files currently in your S3 bucket and writes the csv file to the same S3 bucket'''

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.list_objects_v2(Bucket=bucket)
        #retrieve the list of files in the s3 bucket
        file_list = response['Contents']
        #create a csv file with the list of files in the s3 bucket
        csv_file = 'file_list.csv'
        with open(csv_file, 'w') as f:
            f.write('File Name, Size, Last Modified, ARN, eTag\n')
            for file in file_list:
                f.write(file['Key'] + ', ' + str(file['Size']) + ' bytes, ' + str(file['LastModified']) + ', ' + file['Key'] + ', ' + file['ETag'] + '\n')
        #upload the csv file to the s3 bucket
        s3.upload_file(csv_file, bucket, csv_file)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
