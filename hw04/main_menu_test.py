import shutil
from moto import mock_aws
import boto3
import os
from main_menu import list_buckets, select_bucket, backup_files, list_objects, download_object, generate_presigned_url, delete_object, upload, list_contents, get_file
import pytest

@mock_aws
def test_list_buckets():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='bucket1')
    conn.create_bucket(Bucket='bucket2')

    buckets = list_buckets()
    assert buckets == ['bucket1', 'bucket2']

@mock_aws
def test_list_buckets_no_buckets():
    buckets = list_buckets()
    assert buckets == []

@mock_aws
def test_list_buckets_many_buckets():
    conn = boto3.resource('s3', region_name='us-east-1')
    for i in range(1000):
        conn.create_bucket(Bucket=f'bucket{i}')

    buckets = list_buckets()
    assert len(buckets) == 1000

@mock_aws
def test_select_bucket(monkeypatch):
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    monkeypatch.setattr('builtins.input', lambda _: 'test_bucket')
    assert select_bucket() == 'test_bucket'

@mock_aws
def test_backup_files():
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    with open('test_folder/test_file.txt', 'w') as f:
        f.write('test content')

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    backup_files('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1
    assert list(conn.Bucket('test_bucket').objects.all())[0].key == 'test_file.txt'

    os.remove('test_folder/test_file.txt')
    os.rmdir('test_folder')

@mock_aws
def test_backup_files_no_folder():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')
    backup_files('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0

@mock_aws
def test_backup_files_bucket_nonexistent():
    # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    with open('test_folder/test_file.txt', 'w') as f:
        f.write('test content')
    conn = boto3.resource('s3', region_name='us-east-1')
    backup_files('test_bucket', 'test_folder')
    with pytest.raises(Exception):
        assert len(list(conn.Bucket('test_bucket').objects.all())) == 0



@mock_aws
def test_list_objects():
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='object1', Body=b'content1')
    bucket.put_object(Key='object2', Body=b'content2')

    objects = list_objects('test_bucket')
    assert objects == ['object1', 'object2']

@mock_aws
def test_download_object():
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
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    url = generate_presigned_url('test_bucket', 'test_object')
    assert url.startswith('https://s3.amazonaws.com/test_bucket/')

@mock_aws
def test_delete_object():
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    delete_object('test_bucket', 'test_object')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0

@mock_aws
def test_upload():
     # Check if the test directory exists
    if os.path.exists('test_folder'):
        # If it exists, remove it and all its contents
        shutil.rmtree('test_folder')
    os.mkdir('test_folder')
    os.mkdir('test_folder/subfolder')  # Create a subfolder
    with open('test_folder/subfolder/test_file.txt', 'w') as f:
        f.write('test content')

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')

    upload('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1
    assert list(conn.Bucket('test_bucket').objects.all())[0].key == '/subfolder/test_file.txt'  # Check the key includes the subfolder

    os.remove('test_folder/subfolder/test_file.txt')
    os.rmdir('test_folder/subfolder')  # Remove the subfolder
    os.rmdir('test_folder')

@mock_aws
def test_list_contents():
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