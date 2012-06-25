__author__ = 'Devin'

import os
import json
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render_html(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_json(self, obj):
        json_text = json.dumps(obj)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json_text)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
