from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    flash,
)

import os
from werkzeug import secure_filename
from utils import log   

from models.user import User
from routes.topic import current_user
from routes.topic import login_require
from config import accept_user_file_type
from config import folder_image_name





main = Blueprint("profile", __name__)

@main.route("/", methods=["GET"])
@login_require
def index():
    u = current_user()
    if u.user_image is not None:
        img_url = "../../image/" + u.user_image 
    return make_response(render_template("BBS/profile.html", user=u, img_url=img_url))


def allow_file(filename):
    return filename.split(".")[-1] in accept_user_file_type


@main.route("/addimage", methods=["POST"])
@login_require
def add_image():
    u = current_user()
    file = request.files["file"]
    if file and allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(folder_image_name, filename))
        u.user_image = filename
        u.save()
        return redirect(url_for(".index"))
    else:
        return redirect(url_for(".index"))


@main.route("/<filename>")
def user_img(filename):
    return send_from_directory(folder_image_name, filename)