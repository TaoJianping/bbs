from flask import Flask
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import make_response
from flask import request
from flask import url_for
from flask import session
from flask import abort

import uuid
import yagmail

from models.user import User
from utils import log
from config import mail_password, mail_user


main = Blueprint("login", __name__)



@main.route("/", methods=["GET"])
def index():
    return make_response(render_template("BBS/login.html"))


@main.route("/register", methods=["GET"])
def register():
    return make_response(render_template("BBS/register.html"))


@main.route("/add", methods=["POST"])
def add_user():
    form = request.form
    user = User(form)
    if user.validate_register() is True:
        token = uuid.uuid1()
        user.token = token
        user.hash_password()
        user.save()
        # 邮箱正文
        url = request.host + url_for(".activate_user") + "?user=" + user.email + "&" + "token=" + str(token)
        contents = [url]
        # 发送邮件
        yag = yagmail.SMTP(user=mail_user, password=mail_password, host='smtp.qq.com')
        yag.send(user.email, '验证激活', contents)
        return redirect(url_for(".index"))
    else:
        return redirect(url_for(".register"))


@main.route("/login", methods=["POST"])
def login():
    form = request.form
    user = User(form)
    if user.validate_login() is True:
        session["email"] = form.get("email")
        return redirect(url_for("bbs.index"))
    else:
        return redirect(url_for(".register"))


@main.route("/activate", methods=["GET"])
def activate_user():
    d = request.args
    u = User.find_by(email=d.get("user"))
    if u is None:
        abort(404)
    if d.get("token"):
        token = d.get("token")
    elif d.get("amp;token"):
        token = d.get("amp;token")
    else:
        abort(404)
    print("token is :", token)
    ans = u.activate_user(token)
    if ans == False:
        abort(404)
    return redirect(url_for("bbs.index"))


@main.route("/log_out", methods=["GET"])
def log_out():
    if session.get("email") is not None:
        session.pop("email")
    return redirect(url_for("bbs.index"))
