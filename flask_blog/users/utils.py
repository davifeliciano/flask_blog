import os
import secrets
from PIL import Image
from flask import current_app, render_template
from flask_login import current_user
from flask_mail import Message
from flask_blog import mail


def save_picture(form_picture):
    """Remove old picture, save new picture and return the new filename"""
    old_picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", current_user.image_file
    )
    if current_user.image_file != "default.jpg":
        os.remove(old_picture_path)

    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_filename
    )

    output_size = (512, 512)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(
        subject="Password Reset Request",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )
    message.body = render_template("mail_template.txt", token=token)
    message.html = render_template("mail_template.html", token=token)
    mail.send(message)
