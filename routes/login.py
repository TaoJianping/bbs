from flask import Flask
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import make_response
from flask import request
from flask import url_for
from flask import session

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
        user.hash_password()
        user.save()
        code = uuid.uuid1()
        # 邮箱正文
        url = "http://localhost:2000" + url_for(".activiate_user") + "?user=" + user.email + "&" + "token=" + str(code)
        contents = [url]
        # 发送邮件
        print(contents)
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


@main.route("/activiate", methods=["GET"])
def activiate_user():
    print(request.args)
    return redirect(url_for("bbs.index"))


@main.route("/log_out", methods=["GET"])
def log_out():
    session.pop("username")
    return redirect(url_for("bbs.index"))
