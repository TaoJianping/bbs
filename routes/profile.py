from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    abort,
)

import os
import uuid
from werkzeug import secure_filename
import yagmail
from utils import log   

from models.user import User
from routes.bbs import current_user
from .bbs import login_require
from config import accept_user_file_type
from config import folder_image_name
from config import mail_password, mail_user


from bson.objectid import ObjectId




main = Blueprint("profile", __name__)

@main.route("/", methods=["GET"])
@login_require
def index():
    u = current_user()
    return make_response(render_template("BBS/profile.html", user=u))


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
        u.update()
        return redirect(url_for(".index"))
    else:
        return redirect(url_for(".index"))


@main.route("/<filename>")
def user_img(filename="default.jpg"):
    return send_from_directory(folder_image_name, filename)


@main.route("/edit_user", methods=["post"])
@login_require
def edit_user():
    """
    用户提交表单修改自己的信息
    return
        返回个人信息页面
    """
    user = current_user()
    user = User.find_by(_id=user._id)
    for k, v in request.form.items():
        setattr(user, k, v)
    user.update()
    return redirect(url_for(".index"))


@main.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        user_id = request.args.get("user_id", None)
        u = User.find_by(_id=ObjectId(user_id))
        token = request.args.get("token", None)
        if user_id is None or token is None and u.token != token:
            abort(404)
        return render_template("BBS/change_password.html", user_id=user_id)
    elif request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        u = User.find_by(_id=ObjectId(user_id))
        u.password = password
        u.hash_password()
        u.token = None
        u.update()
        return redirect(url_for(".index"))


@main.route("/send_password_email", methods=["GET"])
@login_require
def send_password_email():
    token = uuid.uuid1()
    user = current_user()
    user.token = token
    user.update()
    # 邮箱正文
    url = request.host + url_for(".change_password") + "?user_id=" + str(user._id) + "&" + "token=" + str(token)
    contents = [url]
    # 发送邮件
    yag = yagmail.SMTP(user=mail_user, password=mail_password, host='smtp.qq.com')
    yag.send(user.email, '修改密码', contents)
    return redirect(url_for(".index"))
