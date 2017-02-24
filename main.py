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
import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(Handler):
    def get(self):
        self.redirect("/blog")

class MainBlog(Handler):
    #def render_posts(self, subject, content, error):
    #   posts = db.GqlQuery("SELECT * FROM Post ORDER BY desc")
    #   self.render("front.html", subject=subject, content=content, error=error, posts=posts)

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        #self.render("front.html", posts=posts)
        t = jinja_env.get_template("front.html")
        content = t.render(posts = posts)
        #self.response.write("posts")
        self.response.write(content)



class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect("/blog")
        else:
            error = "We need a subject and content!"
            self.render_newpost(subject, content, error)

class DisplayPost(Handler):
        def get(self, id):
            post = Post.get_by_id(int(id))

            if not post:
                self.response.write("404 not found")
                return
            else:
                self.render("permalink.html", post = post)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainBlog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', DisplayPost)

], debug=True)
