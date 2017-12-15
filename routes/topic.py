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

from .bbs import login_require
from .bbs import current_user
from utils import log



main = Blueprint("topic", __name__)



@main.route("/write", methods=["GET"])
@login_require
def topic_write():
    return render_template("BBS/topic_write.html")


@main.route("/upload", methods=["post"])
@login_require
def markdown_upload():
    log(request.form)
    return redirect(url_for('.markdown'))

@main.route("/<topic_id>")
def detail(topic_id):
    t = Topic.find_by(_id=ObjectId(topic_id))
    t.view += 1
    t.update()
    r = Reply.find_all(topic_id=ObjectId(topic_id))
    return render_template("BBS/topic_detail.html", t=t, replys=r)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    user = current_user()
    Topic.new(form, user_id=user._id)
    return redirect(url_for("topic.index"))

