from models import Model
from models.reply import Reply
import time


class Topic(Model):
    def __init__(self, form):
        self.title = form.get("title", None)
        self.content = form.get("content", None)
        self.id = form.get("topic_id", None)
        self.ct = int(time.time())        
        self.view = 0

    def get_replynumber(self):
        rn = str(len(Reply.find_all(topic_id=self.id)))
        return rn