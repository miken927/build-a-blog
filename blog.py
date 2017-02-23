import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello Blog!')

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainBlog(webapp2.RequestHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

    if subject and content:
        self.write("thanks!")
    else:
        error = "We need both a subject and content!"
        self.render("front.html", error = error)

class NewPost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
    ('/blog', MainBlog)
    ('/newpost',NewPost)
], debug=True)
