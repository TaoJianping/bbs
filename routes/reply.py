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
from .bbs import login_require, current_user

main = Blueprint("reply", __name__)


@main.route("/add", methods=["POST"])
@login_require
def add():
    form = request.form
    user = current_user()
    reply = Reply.new(form, author_id=user._id)
    return redirect(url_for("topic.detail", topic_id=str(reply.topic_id)))
