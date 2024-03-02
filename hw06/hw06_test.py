import pytest
import os
from http_utils import get, post, delete, read_file_into_base64_string

base_url = 'https://pdj3jncpqb.execute-api.us-east-1.amazonaws.com/dev'
test_bucket = 'hw06-jzhang'
object_name = 'test-object'

def test_list_buckets_method():
    '''Test the list method of the API. It should return a list of buckets.'''

    response = get(f'{base_url}/list')
    print(response)
    assert response['statusCode'] == 200
    assert 'buckets' in response.json()
    bucket_names = response.json()['buckets']
    assert isinstance(bucket_names, list)

def test_post_method():
    '''Test the post method of the API. It should return the bucket name, object name, and object content.'''

    # Check if test-object.txt exists locally and delete it if it does
    try:
        with open('test-object.txt', 'r') as file:
            pass
    except FileNotFoundError:
        pass
    else:
        os.remove('test-object.txt')

    # Create test object
    with open('test-object.txt', 'w') as file:
        file.write('Hello World')

    data = read_file_into_base64_string('test-object.txt')
    response = post(f'{base_url}/{test_bucket}/{object_name}', data)
    assert response.status_code == 200
    assert 'bucketname' in response.json()
    assert response.json()['bucketname'] == test_bucket
    assert 'objectname' in response.json()
    assert response.json()['objectname'] == object_name
    assert 'objectcontent' in response.json()
    assert response.json()['objectcontent'] == data

#def test_delete_method():
    