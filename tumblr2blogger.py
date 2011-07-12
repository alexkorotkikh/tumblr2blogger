import urllib
from xml.dom.minidom import parseString
from xml.dom.minidom import Node

from gdata import service
import gdata
import atom

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
        print url
        print urllib.urlopen(url).read()
        document = parseString(urllib.urlopen(url).read())
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
    def __init__(self, username, password):
        Account.__init__(self, username, password)

        self._blogger_service = service.GDataService(self._username, self._password)
        self._blogger_service.source = 'alexkorotkikh-tumblr2blogger-1.0'
        self._blogger_service.service = 'blogger'
        self._blogger_service.account_type = 'GOOGLE'
        self._blogger_service.server = 'www.blogger.com'
        self._blogger_service.ProgrammaticLogin()
        self._blogger_service.debug = True
        print 'Logged in!'

        self._blog_id = self._get_blog_id()
        print 'Blog ID recieved'

    def upload_posts(self, posts):
        for post in reversed(posts):
            entry = self._create_entry(post)
            self._blogger_service.Post(entry, '/feeds/%s/posts/default' % self._blog_id)

    def _create_entry(self, post):
        entry = gdata.GDataEntry()
        entry.title = atom.Title('xhtml', post._title)
        entry.content = atom.Content(content_type='html', text=post._content)
        return entry

    def _get_blog_id(self):
        query = service.Query()
        query.feed = '/feeds/default/blogs'
        feed = self._blogger_service.Get(query.ToUri())
        return feed.entry[0].GetSelfLink().href.split("/")[-1]




tumblr = TumblrAccount('alexkorotkikh', '')
posts = tumblr.download_posts()

blogger = BloggerAccount('a.korotkikh@gmail.com', '')
blogger.upload_posts(posts)