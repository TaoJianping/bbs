from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)

from bson.objectid import ObjectId
from models.topic import Topic
from models.reply import Reply
from models.board import Board
from models.user import User


from .bbs import login_require
from .bbs import current_user
from utils import log

import markdown



main = Blueprint("topic", __name__)


@main.route("/write", methods=["GET"])
@login_require
def topic_write():
    """
    返回发布新话题的文章页面
    """
    boards = Board.find_all()
    return render_template("BBS/topic_write.html", boards=boards)


@main.route("/<topic_id>")
def detail(topic_id):
    t = Topic.find_by(_id=ObjectId(topic_id))
    t.view += 1
    t.update()
    topic_writer = User.find_by(_id=ObjectId(t.user_id))
    r = Reply.find_all(topic_id=ObjectId(topic_id))
    topic_writer_topics = Topic.find_by_sort("ct", user_id=ObjectId(topic_writer._id))
    if len(topic_writer_topics) > 10:
        topic_writer_topics = topic_writer_topics[:10]
    return render_template("BBS/topic_detail.html", t=t, replys=r, u=topic_writer, ts=topic_writer_topics)


@main.route("/add", methods=["POST"])
@login_require
def add():
    form = request.form
    user = current_user()
    Topic.new(form, user_id=user._id)
    return redirect(url_for("bbs.index"))

