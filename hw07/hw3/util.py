'''Utility functions'''

def get_s3_file_list(bucket_name, s3, file_extension):
    '''Get a list of all files in an S3 bucket with a specific extension'''
    files = []
    for obj in s3.list_objects(Bucket=bucket_name)['Contents']:
        if obj['Key'].endswith(file_extension):
            files.append(obj['Key'])
    return files
