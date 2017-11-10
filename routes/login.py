from flask import Flask
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import make_response
from flask import request
from flask import url_for
from flask import session

from models.user import User 

from utils import log



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
    if user.validate_register() == True:
        user = User.new(form)
        return redirect(url_for(".index"))
    else:
        return redirect(url_for(".register"))


@main.route("/login", methods=["POST"])
def login():
    form = request.form
    u = User(form)
    log(u.validate_login)
    if u.validate_login == True:
        session["username"] = form.get("username")
        log("登录成功")
        return redirect(url_for("topic.index"))
    else:
        log("登录失败")
        return redirect(url_for(".register"))

