import hashlib
from bson import ObjectId

from models import Model

class User(Model):
    def __init__(self, form):
        self.id = form.get("user_id", None)
        self.email = form.get("email", None)
        self.username = self.email
        self.password = form.get("password", None)
        self.user_image = "default.jpg"
        self.level = 0
        self.inbox = []
        self.token = None
        self.following_list = []
        self.follower_list = []

    def validate_register(self):
        if len(self.email) >= 3 and len(self.password) >= 3 and User.find_by(email=self.email) is None:
            return True
        else:
            return False

    def validate_login(self):
        self.hash_password()
        ms = User.all()
        for i in ms:
            if self.email == i.email and self.password == i.password:
                return True
        return False

    def hash_password(self, salt="tao"):
        """
        经过validate_register函数验证是否符合要求之后，把密码加密
        ===
        args
            实例对象
        return
            一个密码加了密的实例对象
        """
        password = (self.password + salt).encode("utf-8")
        hashed_pasword = hashlib.sha1(password).hexdigest()
        self.password = hashed_pasword

    def bind_inbox_item(self, inbox_item):
        """给用户绑定私信，用于后续的载入"""
        self.inbox.append(inbox_item)
        self.update()

    def activate_user(self, token):
        """激活用户"""
        if str(self.token) == str(token):
            self.token = None
            self.level = 1
            self.update()
            return True
        return False

    def toggle_follow_object(self, object_user_id):
        object_user = User.find_by(_id=ObjectId(object_user_id))
        if ObjectId(object_user_id) in self.following_list:
            object_user.follower_list.remove(self._id)
            self.following_list.remove(ObjectId(object_user_id))
        else:
            object_user.follower_list.append(self._id)
            self.following_list.append(ObjectId(object_user_id))
            object_user.update()
            self.update()
        object_user.update()
        self.update()
