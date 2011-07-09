class Post():
    def __init__(self, title, content, tags, date):
        self._title = title
        self._content = content
        self._tags = tags
        self._date = date

class Account():
    def __init__(self, username, password):
        self._username = username
        self._password = password

class TumblrAccount(Account):
    def download_posts(self):
        pass

class BloggerAccount(Account):
    def upload_posts(self, posts):
        pass
