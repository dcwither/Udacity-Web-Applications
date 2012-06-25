__author__ = 'Devin'

from google.appengine.ext import db
import BaseHandler

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    lastModified = db.DateTimeProperty(auto_now=True)
    def rendered_content(self):
        return self.content.replace('\n', '<br>')

    def render(self):
        return BaseHandler.render_str("post.html", post = self)

    def dict_rep(self):
        return  dict(content = self.content,
                        subject = self.subject,
                        created = self.created.strftime("%b %d, %Y"),
                        lastModified = self.lastModified.strftime("%b %d, %Y"))


class NewPostHandler(BaseHandler.BaseHandler):
    def render_Post(self, subject="", content="", error=""):
        self.render_html(template="newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_Post()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = BlogPost(parent=blog_key(), subject=subject, content=content)
            post.put()
            self.redirect("/blog/%s" % post.key().id())
        else:
            self.render_Post(subject=subject, content=content, error="Subject and content please")

class PostHandler(BaseHandler.BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('BlogPost', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
        if self.request.url.endswith('.json'):
            self.render_json(post.dict_rep())
        else:
            self.render_html(template="permalink.html", post=post)
