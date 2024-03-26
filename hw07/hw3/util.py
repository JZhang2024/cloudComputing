'''Utility functions'''
import os
import time

def get_file_list(folder, extension):
    '''Get list of files that have been uploaded to the server'''
    image_list = []
    # folder += "."
    print("folder", folder)
    for image in os.listdir(folder):
        if image.endswith(extension):
            size = str(os.path.getsize(folder + image))
            dt = time.ctime(os.path.getmtime(folder + image))
            # dt = str(time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(filename))))
            image_list.append([image, size, dt])
    return image_list
