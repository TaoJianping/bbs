from models import Model
import time


class Topic(Model):
    def __init__(self, form):
        self.title = form.get("title", None)
        self.content = form.get("content", None)
        self.id = form.get("topic_id", None)
        self.ct = int(time.time())        

