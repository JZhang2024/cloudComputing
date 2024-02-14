import pytest
import datetime
from moto import mock_aws
import boto3
import os
from main_menu import list_buckets, select_bucket, backup_files, list_objects, download_object, generate_presigned_url, delete_object

@mock_aws
def test_list_buckets():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='bucket1')
    conn.create_bucket(Bucket='bucket2')

    buckets = list_buckets()
    assert buckets == ['bucket1', 'bucket2']

@mock_aws
def test_select_bucket(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_bucket')
    assert select_bucket() == 'test_bucket'

@mock_aws
def test_backup_files(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_bucket')
    os.mkdir('test_folder')
    with open('test_folder/test_file.txt', 'w') as f:
        f.write('test content')

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='test_bucket')  # Create the bucket here
    backup_files('test_bucket', 'test_folder')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 1
    assert list(conn.Bucket('test_bucket').objects.all())[0].key == 'test_file.txt'

    os.remove('test_folder/test_file.txt')
    os.rmdir('test_folder')
@mock_aws
def test_list_objects():
    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='object1', Body=b'content1')
    bucket.put_object(Key='object2', Body=b'content2')

    objects = list_objects('test_bucket')
    assert objects == ['object1', 'object2']

@mock_aws
def test_download_object(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_object')

    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    download_object('test_bucket')
    assert os.path.exists('test_object')

    os.remove('test_object')

@mock_aws
def test_generate_presigned_url(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_object')

    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    url = generate_presigned_url('test_bucket', 'test_object')
    assert url.startswith('https://s3.amazonaws.com/test_bucket/')

@mock_aws
def test_delete_object(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test_object')

    conn = boto3.resource('s3', region_name='us-east-1')
    bucket = conn.create_bucket(Bucket='test_bucket')
    bucket.put_object(Key='test_object', Body=b'content')

    delete_object('test_bucket', 'test_object')
    assert len(list(conn.Bucket('test_bucket').objects.all())) == 0