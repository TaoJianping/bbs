from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)

from bson import ObjectId
from models.user import User
from routes.bbs import current_user, login_require
from models.inbox import Inbox


main = Blueprint("inbox", __name__)


@main.route("/", methods=["GET", "POST"])
@login_require
def index():
    """私信主页面"""
    u = current_user()
    if request.method == "GET":
        inbox_items = [Inbox.find_one(_id=i) for i in u.inbox]
        us = User.all()
        for m in us:
            if m.email == u.email:
                us.remove(m)
        return render_template("BBS/inbox.html", users=us, inbox_items=inbox_items, user=u)
    elif request.method == "POST":
        form = request.form
        print(form)
        receiver = User.find_by(_id=ObjectId(request.form.get("chat-people")))
        dialogue_content = request.form.get("dialogue")
        inbox_item = Inbox.get_inbox_item(receiver.email, u.email)
        if inbox_item is None:
            new_item = Inbox.new(receiver.email, u.email, dialogue_content)
            u.bind_inbox_item(new_item._id)
            receiver.bind_inbox_item(new_item._id)
        else:
            inbox_item.append_dialogue(receiver.email, u.email, dialogue_content)
        return redirect(url_for("inbox.index"))


@main.route("/<string:inbox_id>", methods=["GET", "POST"])
def inbox_detail(inbox_id):
    """私信的详细页面"""
    inbox_item = Inbox.find_one(_id=ObjectId(inbox_id))
    u = current_user()
    if u.email in inbox_item.unmarked:
        inbox_item.unmarked.remove(u.email)
        inbox_item.update()
    inbox_items = [Inbox.find_one(_id=i) for i in u.inbox]
    if u.email == inbox_item.players[0]:
        receiver = inbox_item.players[1]
    else:
        receiver = inbox_item.players[0]
    if request.method == "GET":
        us = User.all()
        for m in us:
            if m.email == u.email:
                us.remove(m)
        return render_template("BBS/inbox_detail.html", inbox_items=inbox_items, user=u,
                               inbox_item=inbox_item)
    elif request.method == "POST":
        dialogue_content = request.form.get("inbox-dialogue")
        inbox_item.append_dialogue(receiver, u.email, dialogue_content)
        return redirect(url_for("inbox.inbox_detail", inbox_id=inbox_id))

