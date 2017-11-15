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



main = Blueprint("topic", __name__)


def current_user():
    username = session.get("username", None)
    user = User.find_by(username=username)
    return user


@main.route("/", methods=["GET"])
def index():
    boards = Board.all()
    ms = Topic.all()
    return render_template("BBS/bbs_topic.html", ms=ms, boards=boards)


@main.route("/detail/<int:topic_id>")
def detail(topic_id):
    t = Topic.find_by(id=topic_id)
    t.view += 1
    t.save()
    r = Reply.find_all(topic_id=topic_id)
    return render_template("BBS/topic_detail.html", t=t, replys=r)


@main.route("/build_new_topic", methods=["GET"])
def build_new_topic():
    return render_template("BBS/build_new_topic.html")


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    user = current_user()
    new_topic = Topic.new(form, user_id=user.id)
    return redirect(url_for("topic.index"))





