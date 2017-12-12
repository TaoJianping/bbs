import hashlib

from models import Model
from utils import log

class User(Model):
    def __init__(self, form):
        self.id = form.get("user_id", None)
        self.username = form.get("username", None)
        self.password = form.get("password", None)
        self.level = 1

    def validate_register(self):
        if len(self.username) >= 3 and len(self.password) >= 3:
            return True
        else:
            return False

    def validate_login(self):
        self.hash_password()
        ms = User.all()
        for m in ms:
            if self.username == m.username and self.password == m.password:
                return True

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
