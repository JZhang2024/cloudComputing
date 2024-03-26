'''API Routes'''
from flask import request, render_template
import util

UPLOAD_FOLDER = "static/images/"

def configure_routes(app):
    '''Setup all the API routes'''

    @app.route('/')
    def list_files():
        '''Show the main screen'''
        image_list = util.get_file_list(UPLOAD_FOLDER, ".png")
        print("Images", image_list)
        return render_template("index.html", imagefiles=image_list)

    @app.route('/upload', methods = ['POST'])
    def success():
        '''Process the file upload and navigate back to the main screen'''
        if request.method == 'POST':
            f = request.files['file']
            f.save(UPLOAD_FOLDER + f.filename)
            return list_files()
        return "Operation not supported"
