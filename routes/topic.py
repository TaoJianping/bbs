from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board

from utils import log



main = Blueprint("topic", __name__)


def current_user():
    username = session.get("username", None)
    user = User.find_by(username=username)
    return user

import functools
def login_require(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        u = current_user()
        if u is not None:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login.index"))
    return wrap

def admin_require(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        u = current_user()
        if u is not None and u.level == 10:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login.index"))
    return wrap


@main.route("/", methods=["GET"])
def index():
    boards = Board.all()
    board_id = int(request.args.get("board_id", -1))
    log("asdasd")
    if board_id == 1 or board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    return render_template("BBS/bbs_topic.html", ms=ms, boards=boards)


@main.route("/detail/<int:topic_id>")
def detail(topic_id):
    t = Topic.find_by(id=topic_id)
    t.view += 1
    t.save()
    r = Reply.find_all(topic_id=topic_id)
    return render_template("BBS/topic_detail.html", t=t, replys=r)


@main.route("/build_new_topic", methods=["GET"])
@login_require
def build_new_topic():
    boards = Board.all()
    return render_template("BBS/build_new_topic.html", board=boards)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    user = current_user()
    new_topic = Topic.new(form, user_id=user.id)
    return redirect(url_for("topic.index"))

@main.route("/log_out", methods=["GET"])
def log_out():
    log(session)
    session.pop("username")
    return redirect(url_for("topic.index"))    
        