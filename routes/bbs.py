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


def current_user():
    email = session.get("email", None)
    user = User.find_by(email=email)
    return user


def login_require(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        u = current_user()
        if u is not None and u.level == 1:
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
@main.route("/<string:board_id>/", methods=["GET"])
def index(board_id=None):
    boards = Board.all()
    page = int(request.args.get("page", 0))
    sort = request.args.get("sort", "ct")
    if (board_id is None) or (board_id == "5a1e9237fe3d2659def8f88f"):
        page_number = Topic.get_page_number()
        board = Board.find_by(_id=ObjectId("5a1e9237fe3d2659def8f88f"))  
        ms = Topic.find_byPage(page, sort)
    else:
        if len(board_id) < 12:
            pass
        else:
            page_number = Topic.get_page_number(board_id)
            board = Board.find_by(_id=ObjectId(board_id))
            ms = Topic.find_byPage(page, sort, board_id=ObjectId(board_id))
    return render_template("BBS/bbs.html",filter=board, pagenumber=page_number, sort=sort, ms=ms, boards=boards)
