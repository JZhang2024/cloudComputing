'''hw04/main_menu.py'''

import os
import time
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import BotoCoreError, ClientError

s3 = boto3.resource('s3')

def list_buckets():
    '''List all the buckets in the S3 account.'''
    return [bucket.name for bucket in s3.buckets.all()]

def select_bucket():
    '''Select a bucket from the list of buckets.'''
    while True:
        bucket_name = input("Enter the bucket name: ")
        if not bucket_name:
            print("Bucket name cannot be empty. Please try again.")
            continue
        if bucket_name not in list_buckets():
            print("Bucket does not exist. Please try again.")
            continue
        return bucket_name

def backup_files(bucket_name, folder_path):
    '''Backup files from a folder to a bucket in S3.'''
    s3_client = boto3.client('s3')
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    if bucket_name not in list_buckets():
        print("Bucket does not exist.")
        return
    #splits large files into smaller chunks for faster upload
    transfer_config = boto3.s3.transfer.TransferConfig(multipart_threshold=1024**3,
                                                       multipart_chunksize=1024**3)
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                try:
                    s3_client.upload_fileobj(data,
                                      bucket_name,
                                      full_path[len(folder_path)+1:],
                                      Config=transfer_config)
                    print(f"File {full_path} backed up successfully.")
                except NoCredentialsError:
                    print("Credentials not available")

def list_objects(bucket_name):
    '''List all the objects in a bucket.'''
    bucket = s3.Bucket(bucket_name)
    return [obj.key for obj in bucket.objects.all()]

def download_object(bucket_name, object_name):
    '''Download an object from a bucket.'''
    try:
        s3.Bucket(bucket_name).download_file(object_name, object_name)
        print("Download successful")
    except NoCredentialsError:
        print("Credentials not available")

def generate_presigned_url(bucket_name, object_name):
    '''Generate a presigned URL for an object in a bucket.'''
    try:
        url = s3.meta.client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"

def list_object_version_info(bucket_name, object_name):
    '''List object version info.'''
    try:
        versions = s3.Bucket(bucket_name).object_versions.filter(Prefix=object_name)
        return versions
    except NoCredentialsError:
        return "Credentials not available"

def delete_object(bucket_name, object_name):
    '''Delete an object from a bucket.'''
    try:
        s3.Bucket(bucket_name).delete_objects(Delete={'Objects': [{'Key': object_name}]})
        print("Object deleted successfully")
    except NoCredentialsError:
        print("Credentials not available")



def upload(bucket_name, local_folder_name):
    '''Uploads a folder to an S3 bucket.
    Files are uploaded one at a time and folder structure is preserved.'''
    s3_client = boto3.client('s3')
    #splits large files into smaller chunks for faster upload
    transfer_config = boto3.s3.transfer.TransferConfig(multipart_threshold=1024**3,
                                                       multipart_chunksize=1024**3)
    for subdir, _, files in os.walk(local_folder_name):
        for file in files:
            full_path = os.path.join(subdir, file)
            key = full_path[len(local_folder_name):]
            s3_obj = s3.Object(bucket_name, key)
            if s3_obj.key not in list_objects(bucket_name):
                pass
            elif s3_obj.last_modified.timestamp() > os.path.getmtime(full_path):
                continue  # Skip this file because it has not changed
            for _ in range(3):  # Retry up to 3 times
                try:
                    with open(full_path, 'rb') as data:
                        s3_client.upload_fileobj(data,
                                          bucket_name,
                                          key,
                                          Config=transfer_config)
                    break  # The upload was successful, so we break out of the retry loop
                except BotoCoreError as upload_exception:
                    print(f"Error uploading {full_path} to {bucket_name}: {upload_exception}")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                except IOError as upload_exception:
                    print(f"Error reading file {full_path}: {upload_exception}")
                    break  # There's no point in retrying if we can't read the file

def list_contents(bucket_name, server_folder_name):
    '''List the contents of a folder in an S3 bucket.'''
    return [obj.key for obj in s3.Bucket(bucket_name).objects.filter(Prefix=server_folder_name)]

def get_file(bucket_name, server_folder_name, file_name):
    '''Download a file from a folder in an S3 bucket.'''
    try:
        s3.Object(bucket_name, server_folder_name + '/' + file_name).load()
        s3.Bucket(bucket_name).download_file(server_folder_name + '/' + file_name, file_name)
        print("File downloaded successfully")
    except ClientError as not_found_exception:
        print("Either the specified folder/file does not exist or another error occurred: ",
              not_found_exception)

def main_menu():
    '''Main menu for the S3 application.'''
    while True:
        print("1. List all buckets")
        print("2. Backup files to a bucket")
        print("3. List all objects in a bucket")
        print("4. Download an object from a bucket")
        print("5. Generate a presigned URL for an object")
        print("6. List object version info")
        print("7. Delete an object")
        print("8. Upload a folder to an S3 bucket")
        print("9. List the contents of a folder in an S3 bucket")
        print("10. Download a file from a folder in an S3 bucket")
        print("11. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            buckets = list_buckets()
            for bucket in buckets:
                print(bucket)
        elif choice == 2:
            bucket_name = select_bucket()
            folder_path = input("Enter the path of the folder: ")
            backup_files(bucket_name, folder_path)
        elif choice == 3:
            bucket_name = select_bucket()
            object_keys = list_objects(bucket_name)
            for key in object_keys:
                print(key)
        elif choice == 4:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object you want to download: ")
            download_object(bucket_name, object_name)
        elif choice == 5:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            url = generate_presigned_url(bucket_name, object_name)
            print(url)
        elif choice == 6:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            versions = list_object_version_info(bucket_name, object_name)
            if versions == "Credentials not available":
                print("Credentials not available")
                continue
            for version in versions:
                print(version.get())
        elif choice == 7:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            delete_object(bucket_name, object_name)
        elif choice == 8:
            bucket_name = select_bucket()
            local_folder_name = input("Enter the name of the folder: ")
            upload(bucket_name, local_folder_name)
        elif choice == 9:
            bucket_name = select_bucket()
            server_folder_name = input("Enter the name of the folder: ")
            contents = list_contents(bucket_name, server_folder_name)
            for content in contents:
                print(content)
        elif choice == 10:
            bucket_name = select_bucket()
            server_folder_name = input("Enter the name of the folder: ")
            file_name = input("Enter the name of the file: ")
            get_file(bucket_name, server_folder_name, file_name)
        elif choice == 11:
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main_menu()
