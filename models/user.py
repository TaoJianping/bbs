from models import Model
from utils import log

class User(Model):
    def __init__(self, form):
        self.id = form.get("user_id", None)
        self.username = form.get("username", None)
        self.password = form.get("password", None)

    def validate_register(self):
        if len(self.username) >= 3 and len(self.password) >= 3:
            return True
        else:
            return False

    def validate_login(self):
        log("使用了这个验证登录函数")
        ms = User.all()
        for m in ms:
            if self.username == m.username and self.password == m.password:
                return True 


