import boto3
import os
from botocore.exceptions import NoCredentialsError

s3 = boto3.resource('s3')

def list_buckets():
    for bucket in s3.buckets.all():
        print(bucket.name)

def select_bucket():
    bucket_name = input("Enter the bucket name: ")
    return bucket_name

def backup_files(bucket_name):
    folder_path = input("Enter the path of the folder you want to backup: ")
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                s3.Bucket(bucket_name).put_object(Key=full_path[len(folder_path)+1:], Body=data)

def list_objects(bucket_name):
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(obj.key)

def download_object(bucket_name):
    object_name = input("Enter the name of the object you want to download: ")
    try:
        s3.Bucket(bucket_name).download_file(object_name, object_name)
        print("Download successful")
    except NoCredentialsError:
        print("Credentials not available")

def generate_presigned_url(bucket_name, object_name):
    try:
        url = s3.meta.client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
        print(url)
    except NoCredentialsError:
        print("Credentials not available")

def list_object_version_info(bucket_name, object_name):
    try:
        versions = s3.Bucket(bucket_name).object_versions.filter(Prefix=object_name)
        for version in versions:
            print(version.get())
    except NoCredentialsError:
        print("Credentials not available")

def delete_object(bucket_name, object_name):
    try:
        s3.Bucket(bucket_name).delete_objects(Delete={'Objects': [{'Key': object_name}]})
        print("Object deleted successfully")
    except NoCredentialsError:
        print("Credentials not available")

def main_menu():
    while True:
        print("1. List all buckets")
        print("2. Backup files to a bucket")
        print("3. List all objects in a bucket")
        print("4. Download an object from a bucket")
        print("5. Generate a presigned URL for an object")
        print("6. List object version info")
        print("7. Delete an object")
        print("8. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            list_buckets()
        elif choice == 2:
            bucket_name = select_bucket()
            backup_files(bucket_name)
        elif choice == 3:
            bucket_name = select_bucket()
            list_objects(bucket_name)
        elif choice == 4:
            bucket_name = select_bucket()
            download_object(bucket_name)
        elif choice == 5:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            generate_presigned_url(bucket_name, object_name)
        elif choice == 6:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            list_object_version_info(bucket_name, object_name)
        elif choice == 7:
            bucket_name = select_bucket()
            object_name = input("Enter the name of the object: ")
            delete_object(bucket_name, object_name)
        elif choice == 8:
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main_menu()