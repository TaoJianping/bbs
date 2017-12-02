import time
from bson.objectid import ObjectId

from utils import log
from models import Model
from models.user import User



class Reply(Model):
    def __init__(self, form):
        self.content = form.get("content", None)
        self.id = form.get("reply_id", None)
        self.ct = int(time.time())
        self.topic_id = ObjectId(form.get("topic_id", None))
        self.author_id = None

    def get_replymaker(self):
        user = User.find_by(_id=self.author_id)
        return user.username

