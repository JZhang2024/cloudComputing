'''
Utility module for making http calls from python.
Students may pull this file into their own repos and modify it as they
wish to math their REST API implementation.

NOTE: you will need to run:   pip3 install requests
to pull in the requests model. Then, you will need to create a requirements.txt
and inclue something like the following as the only contents:

requests==2.28.1

That will allow GitHub Ations to pull that module in when using this file.

I suggest placing the requirements.txt in your specific HWXX folder. Then
you can use something like this in your yaml:

        run: |
          python -m pip install --upgrade pip
          pip install pytest
          if [ -f HW06/requirements.txt ]; then pip install -r HW06/requirements.txt; fi

'''
import requests
import base64

#https://www.datacamp.com/tutorial/making-http-requests-in-python

def get(url):
    '''Make a simple GET request'''
    print("GET", url)
    response = requests.get(url)
    return response.json()

def post(url, post_data):
    '''Make POST request. Pass post data.'''
    print("POST", url)
    post_response = requests.post(url, json=post_data)
    # print("Post Response:", post_response.json())
    return post_response.json()

def delete(url, data):
    '''Make DEL request. Pass data.'''
    print("DEL", url)
    delete_response = requests.delete(url, json=data)
    return delete_response.json()

def create_post_data_for_list_objects(bucket, file):
    '''Create the post data for a call to Listing Objects in a bucket'''
    return { "bucket": bucket, "file_name": file }

def create_post_data_for_post_object(bucket, file, content):
    '''Create the post data for a call to posting an object'''
    return { "bucket": bucket, "file_name": file, "body": content }

def create_data_for_del_object(bucket, file):
    '''Create the data for deleting an object from a bucket'''
    return { "bucket": bucket, "file_name": file }

def read_file_into_base64_string(file_path):
    '''
    Pass a full file path and file name. Returns the base64 string
    that can be placed into the "content" parameter that goes into
    the body of the create_post_data_for_post_object call

    Note: On the receiving end (your python lambda function called
    by API Gateway), you can use the following code to decode:

    import base64
    file_content = base64.b64decode(event['body-json']['body'])
    '''
    image_file= open(file_path,"rb")
    image_data_binary = image_file.read()
    return (base64.b64encode(image_data_binary)).decode('ascii')