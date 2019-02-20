import secrets
import os
from flask import url_for, current_app
from PIL import Image

def save_picture(pic_form):
    """
    Renames file to a generated name and saves it in static/img/profile_pics folder
    """
    random_hex = secrets.token_hex(8) # 8 bytes

    _ , file_ext = os.path.splitext(pic_form.filename) # underscore for variable which we don't use by convention

    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path,"static/img/profile_pics", picture_filename)

    output_size = (256,256)
    img = Image.open(pic_form)
    img.thumbnail(output_size)

    img.save(picture_path)

    return picture_filename
