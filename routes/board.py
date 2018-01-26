from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)

from models.user import User
from models.board import Board
from .bbs import admin_require, current_user

main = Blueprint("board", __name__)


@main.route("/board", methods=["GET"])
@admin_require
def board():
    u = current_user()
    if u == None:
        return redirect(url_for("bbs.index"))
    else:
        return render_template("BBS/board.html")
    

@main.route("/add", methods=["POST"])
@admin_require
def add():
    form = request.form
    reply = Board.new(form)
    return redirect( url_for("bbs.index"))