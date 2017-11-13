from models import Model
from models.user import User 
import time


class Reply(Model):
    def __init__(self, form):
        self.content = form.get("content", None)
        self.id = form.get("reply_id", None)
        self.ct = int(time.time())
        self.topic_id = int(form.get("topic_id", -1))
        self.author_id = None

    def get_replymaker(self):
        user = User.find_by(id=self.author_id)
        return user.username

