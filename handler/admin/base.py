import tornado.web
import dao.dbase
import hashlib


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_current_user(self):
        user_tab = dao.dbase.BaseDBSupport().db["user"]
        username = self.get_secure_cookie("user")
        token = self.get_secure_cookie("token")
        if username is None or token is None:
            return None

        user = user_tab.find_one({"email": username})
        if user is None:
            return None

        if user["token"] != token:
            return None

        before = token[:len(token) - 16]
        sha = hashlib.sha256(username + self.request.remote_ip).hexdigest()
        if before != sha:
            return None

        return username