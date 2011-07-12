import urllib
from xml.dom.minidom import parseString
from xml.dom.minidom import Node

TUMBLR_URL = 'http://{username}.tumblr.com/api/'

class Post():
    def __init__(self, title, content, tags, date):
        self._title = title
        self._content = content
        self._tags = tags
        self._date = date

    def __unicde__(self):
        return self._date + ": " + self._title

class Account():
    def __init__(self, username, password):
        self._username = username
        self._password = password

class TumblrAccount(Account):
    def download_posts(self):
        base_url = (TUMBLR_URL + 'read').format(username=self._username)
        url = self._create_url(base_url, num=50, type='text')
        document = parseString(urllib.urlopen(url).read())
        # print urllib.urlopen(url).read()
        post_nodes = [post_node for post_node in document.getElementsByTagName("post")]
        return [self._parse_post_node(post_node) for post_node in post_nodes]
          

    def _create_url(self, base_url, **params):
        url = base_url
        params_string = ""
        for param in params.keys():
            params_string += param + '=' + str(params[param]) + "&"
        if params_string != "":
            url += "?" + params_string[:-1]
        return url

    def _parse_post_node(self, post_node):
        try:
            title = post_node.getElementsByTagName("regular-title")[0].childNodes[0].data
        except IndexError:
            title = ""
        content = post_node.getElementsByTagName("regular-body")[0].childNodes[0].data
        tags = [tag_node.childNodes[0].data for tag_node in post_node.getElementsByTagName("tag")]
        date = post_node.getAttribute("date-gmt")

        return Post(title, content, tags, date)


class BloggerAccount(Account):
    def upload_posts(self, posts):
        pass


tumblr = TumblrAccount('alexkorotkikh', '')
for post in tumblr.download_posts():
    print post.__unicde__()