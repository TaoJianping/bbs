import functools
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
)

from models.user import User
from models.topic import Topic
from models.board import Board

from bson.objectid import ObjectId




main = Blueprint("bbs", __name__)


def current_user():
    email = session.get("email", None)
    user = User.find_by(email=email)
    return user


def login_require(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        u = current_user()
        if u is not None and u.level > 0:
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
    page = int(request.args.get("page", 1))
    if page < 2:
        former_page = None
    else:
        former_page = page - 1
    sort = request.args.get("sort", "ct")
    if (board_id is None) or (board_id == "5a6b00b965d4400b98bcf605"):
        page_number = Topic.get_page_number()
        board = Board.find_by(_id=ObjectId("5a6b00b965d4400b98bcf605"))
        ms = Topic.find_byPage(page, sort)
    else:
        if len(board_id) < 12:
            pass
        else:
            page_number = Topic.get_page_number(board_id)
            board = Board.find_by(_id=ObjectId(board_id))
            ms = Topic.find_byPage(page, sort, board_id=ObjectId(board_id))
    if page_number == page:
        next_page = None
    else:
        next_page = page + 1
    return render_template("BBS/bbs.html",filter=board, pagenumber=page_number,
                           sort=sort, ms=ms, boards=boards, next_page=next_page,
                           former_page=former_page)


@main.route("/search", methods=["GET"])
def search():
    all_topics = Topic.all()
    ret = []
    query = request.args.get("query").lower()
    for i in all_topics:
        if query in i.title.lower():
            ret.append(i)
    return render_template("BBS/search.html", ms=ret)


@main.route("/follow", methods=["POST"])
def follow():
    object_user_id = request.form.get("object_user_id")
    topic_id = request.form.get("topic_id")
    u = current_user()
    if str(u._id) == object_user_id:
        abort(404)
    u.toggle_follow_object(object_user_id)
    return redirect(url_for("topic.detail", topic_id=topic_id))