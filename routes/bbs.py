import functools
import math
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)

from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board

from bson.objectid import ObjectId

from utils import log



main = Blueprint("bbs", __name__)


from utils import log


def current_user():
    email = session.get("email", None)
    user = User.find_by(email=email)
    return user


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
    board_id = request.args.get("board_id", None)
    board = Board.find_by(_id=ObjectId(board_id))
    page = int(request.args.get("page", 0))
    if (board_id == "5a1e9237fe3d2659def8f88f") or (board_id is None):
        topic_number = Topic.get_collection_number()
        page_number = math.ceil(topic_number/7)
        ms = Topic.find_byPage(page)
    else:
        topic_number = Topic.get_collection_number(board_id=ObjectId(board_id))
        page_number = math.ceil(topic_number/7)
        ms = Topic.find_byPage(page, board_id=ObjectId(board_id))
    return render_template("BBS/bbs.html", ms=ms, boards=boards, filter=board, pagenumber=page_number)


@main.route("/log_out", methods=["GET"])
def log_out():
    log(session)
    session.pop("username")
    return redirect(url_for("topic.index"))
