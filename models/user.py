import hashlib

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
        print("用户的token是", self.token)
        print("传过来的token是", token)
        if str(self.token) == str(token):
            self.token = None
            self.level = 1
            self.update()
            return True
        return False
