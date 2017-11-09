from models import Model
import time


class Topic(Model):
    def __init__(self, form):
        self.title = form.get("title", None)
        self.topic_id = form.get("topic_id", None)
        self.ct = int(time.time())
        self.author_id = form.get("author_id", None)
        

