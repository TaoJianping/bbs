from models import Model
from models.user import User 
import time


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.ct = int(time.time())
        self.board_name = form.get("board_name", None)

