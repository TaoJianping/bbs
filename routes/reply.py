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
from models.reply import Reply

main = Blueprint("reply", __name__)


def current_user():
    username = session.get("username", None)
    user = User.find_by(username=username)
    return user


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    user = current_user()
    reply = Reply.new(form, author_id=user.id)
    return redirect( url_for("topic.index"))



