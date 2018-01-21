import time
import math
from bson.objectid import ObjectId

from models import Model
from models.reply import Reply




class Topic(Model):
    def __init__(self, form, **kwargs):
        self.title = form.get("title", None)
        self.content = form.get("test-editormd-html-code", None)
        self.id = form.get("topic_id", None)
        self.ct = int(time.time())        
        self.view = 0
        self.board_id = ObjectId(form.get("board_id", None))
        self.rt = None

    def get_replynumber(self):
        rn = str(len(Reply.find_all(topic_id=ObjectId(self._id))))
        return rn

    @classmethod
    def get_page_number(cls, board_id=None):
        """
        任何
        """
        if board_id == None:
            topic_number = cls.get_collection_number()
        else:
            topic_number = cls.get_collection_number(board_id=ObjectId(board_id))
        page_number = math.ceil(topic_number/7)
        return page_number


