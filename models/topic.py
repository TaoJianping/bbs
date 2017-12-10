from bson.objectid import ObjectId

from models import Model
from models.reply import Reply
import time


class Topic(Model):
    def __init__(self, form, **kwargs):
        self.title = form.get("title", None)
        self.content = form.get("content", None)
        self.id = form.get("topic_id", None)
        self.ct = int(time.time())        
        self.view = 0
        self.board_id = ObjectId(form.get("board_id", None))

    def get_replynumber(self):
        rn = str(len(Reply.find_all(topic_id=ObjectId(self._id))))
        return rn
