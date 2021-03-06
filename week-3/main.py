#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import BlogPost
from google.appengine.ext import db
import webapp2
import BaseHandler

class MainHandler(BaseHandler.BaseHandler):
    def get(self):
        self.redirect('/blog')

class BlogHandler(BaseHandler.BaseHandler):
    def get(self):
        posts = db.GqlQuery("select * from BlogPost order by created desc limit 10")
        self.render("Blog.html", posts=posts)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/blog', BlogHandler),
                               ('/blog/newpost', BlogPost.NewPostHandler),
                               ('/blog/([0-9]+)', BlogPost.PostHandler)],
                              debug=True)
