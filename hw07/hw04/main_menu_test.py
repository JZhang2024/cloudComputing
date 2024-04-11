'''test_main_menu.py - This file contains the tests for the main_menu.py file.
The tests are written using the pytest framework and the moto library to mock AWS services'''

import shutil
import os
from moto import mock_aws
import boto3
import pytest
from main_menu import (
    list_buckets,
    select_bucket,
    backup_files,
    list_objects,
    download_object,
    generate_presigned_url,
    delete_object,
    upload,
    list_contents,
    get_file
)

@mock_aws
def test_list_buckets():
    '''Test the list_buckets function.
    This function should return a list of all the buckets in the account.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='bucket1')
    conn.create_bucket(Bucket='bucket2')

    buckets = list_buckets()
    assert buckets == ['bucket1', 'bucket2']

@mock_aws
def test_list_buckets_no_buckets():
    '''Test the list_buckets function when there are no buckets in the account.
    This function should return an empty list.'''
    buckets = list_buckets()
    assert buckets == []

@mock_aws
def test_list_buckets_many_buckets():
    '''Test the list_buckets function when there are many buckets in the account.
    This function should return a list of all the buckets in the account.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    for i in range(1000):
        conn.create_bucket(Bucket=f'bucket{i}')

    buckets = list_buckets()
    assert len(buckets) == 1000

@mock_aws
def test_select_bucket(monkeypatch):
    '''Test the select_bucket function.
    This function should prompt the user to select a bucket and return the selected bucket.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    monkeypatch.setattr('builtins.input', lambda _: 'test_bucket')
    assert select_bucket() == 'test_bucket'

@mock_aws
def test_backup_files():
    '''Test the backup_files function.
    This function should backup the files in the specified folder to the specified bucket.'''
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    with open('test_folder/test_file.txt', 'w') as test_file:
        test_file.write('test content')

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    backup_files('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1
    assert list(conn.Bucket('test_bucket').objects.all())[0].key == 'test_file.txt'

    os.remove('test_folder/test_file.txt')
    os.rmdir('test_folder')

@mock_aws
def test_backup_files_no_folder():
    '''Test the backup_files function when the specified folder does not exist.
    This function should print an error message and return.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    backup_files('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0

@mock_aws
def test_backup_files_bucket_nonexistent():
    '''Test the backup_files function when the specified bucket does not exist.
    This function should print an error message and return.'''
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    with open('test_folder/test_file.txt', 'w') as test_file:
        test_file.write('test content')
    conn = boto3.resource('s3', region_name='us-east-1')
    backup_files('test_bucket', 'test_folder')
    with pytest.raises(Exception):
        assert len(list(conn.Bucket('test_bucket').objects.all())) == 0



@mock_aws
def test_list_objects():
    '''Test the list_objects function.
    This function should return a list of all the objects in the specified bucket.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='object1', Body=b'content1')
    bucket.put_object(Key='object2', Body=b'content2')

    objects = list_objects('test_bucket')
    assert objects == ['object1', 'object2']

@mock_aws
def test_download_object():
    '''Test the download_object function.
    This function should download the specified object from the specified bucket.'''
    if os.path.exists('test_object'):
        os.remove('test_object')
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    download_object('test_bucket', 'test_object')
    assert os.path.exists('test_object')

    os.remove('test_object')

@mock_aws
def test_generate_presigned_url():
    '''Test the generate_presigned_url function.
    This function should generate a presigned URL for the specified object'''
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    url = generate_presigned_url('test_bucket', 'test_object')
    assert url.startswith('https://s3.amazonaws.com/test_bucket/')

@mock_aws
def test_delete_object():
    '''Test the delete_object function.
    This function should delete the specified object from the specified bucket.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    delete_object('test_bucket', 'test_object')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0

@mock_aws
def test_upload():
    '''Test the upload function.
    This function should upload the files in the specified folder to the specified bucket.'''
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    os.mkdir('test_folder/subfolder')  # Create a subfolder
    with open('test_folder/subfolder/test_file.txt', 'w') as test_file:
        test_file.write('test content')

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')

    upload('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1
    # Check the key includes the subfolder
    assert list(conn.Bucket('test_bucket').objects.all())[0].key == '/subfolder/test_file.txt'

    shutil.rmtree('test_folder')

@mock_aws
def test_upload_no_folder():
    '''Test the upload function when the specified folder does not exist.
    This function should return without uploading anything.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    upload('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0

@mock_aws
def test_upload_large_file():
    '''Test the upload function when the specified folder contains a large file.
    This function should split the file into smaller chunks
    and upload them to the specified bucket.'''
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    os.mkdir('test_folder/subfolder')  # Create a subfolder
    #create large file 5GB
    with open('test_folder/subfolder/large_file.txt', 'wb') as test_file:
        test_file.write(os.urandom(5 * 1024**3))

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')

    upload('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1

    shutil.rmtree('test_folder')

@mock_aws
def test_list_contents():
    '''Test the list_contents function.
    This function should return a list of all the objects in the specified folder.'''
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    folder_name = 'test_folder'
    object1_key = 'test_folder/object1'
    object2_key = 'test_folder/object2'

    # Create the folder structure and objects
    bucket.put_object(Key=object1_key, Body=b'content1')
    bucket.put_object(Key=object2_key, Body=b'content2')

    # Test list_contents function
    objects = list_contents('test_bucket', folder_name)
    assert objects == [object1_key, object2_key]

@mock_aws
def test_get_file():
    '''Test the get_file function.
    This function should download the specified object from the specified bucket.'''
    if os.path.exists('test_file.txt'):
        os.remove('test_file.txt')

    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    folder_name = 'test_folder'
    object_key = 'test_folder/test_file.txt'
    bucket.put_object(Key=object_key, Body=b'content')

    get_file('test_bucket', folder_name, 'test_file.txt')
    assert os.path.exists('test_file.txt')

    os.remove('test_file.txt')

@mock_aws
def test_get_file_nonexistent():
    '''Test the get_file function when the specified object does not exist.
    This function should print an error message and return.'''
    get_file('test_bucket', 'test_folder', 'test_file.txt')
    assert not os.path.exists('test_file.txt')
