__author__ = 'Devin'

from google.appengine.ext import db
import BaseHandler
import webapp2

class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class NewPostHandler(BaseHandler.BaseHandler):
    def render_Post(self, subject="", content="", error=""):
        self.render(template="NewPost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_Post()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = BlogPost(subject=subject, content=content)
            post.put()
            self.redirect("/blog/%s" % post.key().id())
        else:
            self.render_Post(subject=subject, content=content, error="Subject and content please")

class PostHandler(BaseHandler.BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            self.render(template="BlogPost.html", post=post)
        else:
            self.redirect("/blog")
