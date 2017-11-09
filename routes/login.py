from flask import Flask
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import make_response
from utils import log



main = Blueprint("login", __name__)

@main.route("/", methods=["GET"])
def index():
    return make_response(render_template("BBS/login.html"))


@main.route("/register", methods=["GET"])
def register():
    return make_response(render_template("BBS/register.html"))
