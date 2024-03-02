import pytest
import os
from http_utils import get, post, delete, read_file_into_base64_string, create_data_for_del_object, create_post_data_for_post_object

base_url = 'https://pdj3jncpqb.execute-api.us-east-1.amazonaws.com/dev'
test_bucket = 'hw06-jzhang'
object_name = 'test-object'

def test_list_buckets_method():
    '''Test the list method of the API. It should return a list of buckets.'''

    response = get(f'{base_url}/list')
    print(response)
    assert response['statusCode'] == 200
    assert 'buckets' in response['body']

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
    post_data = create_post_data_for_post_object(test_bucket, object_name, data)
    response = post(f'{base_url}/{test_bucket}', post_data)
    print(response)
    assert response['statusCode'] == 200
    assert 'bucketname' in response['body']
    assert response['bucketname'] == test_bucket
    assert 'objectname' in response['body']
    assert response['body']['objectname'] == object_name
    assert 'objectcontent' in response
    assert response['body']['objectcontent'] == data

    os.remove('test-object.txt')


#def test_delete_method():
    