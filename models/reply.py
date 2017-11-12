from models import Model
import time


class Reply(Model):
    def __init__(self, form):
        self.content = form.get("content", None)
        self.id = form.get("reply_id", None)
        self.ct = int(time.time())
        self.topic_id = int(form.get("topic_id", -1))
        self.author_id = None

