from models import Model

class User(Model):
    def __init__(self, form):
        self.id = form.get("user_id", None)
        self.username = form.get("username", None)
        self.password = form.get("password", None)