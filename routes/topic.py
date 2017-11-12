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

main = Blueprint("topic", __name__)


def current_user():
    username = session.get("username", None)
    user = User.find_by(username=username)
    return user


@main.route("/", methods=["GET"])
def index():
    ms = Topic.all()
    return render_template("BBS/bbs_topic.html", ms=ms)


@main.route("/detail/<int:topic_id>")
def detail(topic_id):
    t = Topic.find_by(id=topic_id)
    return render_template("BBS/topic_detail.html", t=t)


@main.route("/build_new_topic", methods=["GET"])
def build_new_topic():
    return render_template("BBS/build_new_topic.html")


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    user = current_user()
    new_topic = Topic.new(form, user_id=user.id)
    return redirect(url_for("topic.index"))





