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
from models.board import Board

main = Blueprint("board", __name__)


def current_user():
    username = session.get("username", None)
    user = User.find_by(username=username)
    return user


@main.route("/board", methods=["GET"])
def board():
    u = current_user()
    if u == None:
        redirect(url_for("topic.index"))
    else:
        return render_template("BBS/board.html")
    

@main.route("/add", methods=["POST"])
def add():
    form = request.form
    reply = Board.new(form)
    return redirect( url_for("topic.index"))