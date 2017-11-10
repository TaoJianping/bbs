from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

main = Blueprint("topic", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("BBS/bbs_topic")
