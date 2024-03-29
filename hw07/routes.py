'''API Routes'''
from flask import request, render_template
import util
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "hw07-jzhang"

def configure_routes(app):
    '''Setup all the API routes'''

    @app.route('/')
    def list_files():
        '''Show the main screen'''
        image_list_png = util.get_s3_file_list(BUCKET_NAME, s3, ".png")
        image_list_jpg = util.get_s3_file_list(BUCKET_NAME, s3, ".jpg")
        image_list = image_list_png + image_list_jpg
        print("Images", image_list)
        return render_template("index.html", imagefiles=image_list)

    @app.route('/upload', methods = ['POST'])
    def success():
        '''Process the file upload and navigate back to the main screen'''
        if request.method == 'POST':
            f = request.files['file']
            s3.upload_fileobj(f, BUCKET_NAME, f.filename)
            return list_files()
        return "Operation not supported"
