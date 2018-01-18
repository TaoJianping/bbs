from models import Model, db
import time


class Inbox(Model):
    def __init__(self):
        self.players = []
        self.dialogue = []
        self.ct = int(time.time())
        self.ut = int(time.time())
        self.unmarked = []

    @classmethod
    def get_inbox_item(cls, receiver_mail, sender_mail):
        email_query = [receiver_mail, sender_mail]
        query2 = email_query[::-1]
        if Inbox.find_one(players=email_query) is not None:
            return Inbox.find_one(players=email_query)
        elif Inbox.find_one(players=query2) is not None:
            return Inbox.find_one(players=query2)
        else:
            return None

    @classmethod
    def new(cls, receiver_email, sender_email, content):
        new_inbox = Inbox()
        new_inbox.players.append(sender_email)
        new_inbox.players.append(receiver_email)
        new_inbox.dialogue.append({
            "sender" : sender_email,
            "receiver" : receiver_email,
            "content" : content,
            "ct" : int(time.time()),
        })
        new_inbox.unmarked.append(receiver_email)
        new_inbox.save()
        saved_inbox_item = Inbox.get_inbox_item(receiver_email, sender_email)
        return saved_inbox_item

    def append_dialogue(self, receiver_email, sender_email, content):
        dialogue_item = dict(
            sender = sender_email,
            receiver = receiver_email,
            content = content,
            ct = int(time.time()),
        )
        self.dialogue.append(dialogue_item)
        if receiver_email in self.unmarked:
            pass
        else:
            self.unmarked.append(receiver_email)
        self.update()

    @classmethod
    def find_one(cls, **kwargs):
        """
        根据给定的关键词参数组成的dict,在数据库中寻找相应的数据
        ===
        args
            kwargs: 关键词参数, 给定的查询条件,如author_id=ObjectId(***)
        return
            model: 通过找到的数据重构的一系列实例对象
        """
        data = db[cls.__name__].find_one(kwargs)
        if data is not None:
            i = Inbox()
            for k, v in data.items():
                setattr(i, k, v)
            return i
        return None

    def toggle_mark(self):
        if self.mark == "未读":
            self.mark = "已读"
            self.update()
        elif self.mark == "已读":
            self.mark = "未读"
            self.update()

    @staticmethod
    def dialogue_time(t):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))





        