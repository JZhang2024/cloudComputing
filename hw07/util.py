'''Utility functions'''

def get_s3_file_list(bucket_name, s3_client, file_extension):
    '''Get the list of files in the S3 bucket'''
    files = []
    result = s3_client.list_objects(Bucket=bucket_name)

    if 'Contents' not in result:
        return files

    for obj in result['Contents']:
        if obj['Key'].endswith(file_extension):
            file_info = {
                'name': obj['Key'],
                'size': obj['Size'],
                'last_modified': obj['LastModified'],
                'url': s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': obj['Key']},
                                                        ExpiresIn=3600)
            }
            files.append(file_info)
    return files
