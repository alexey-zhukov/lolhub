from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

import loluser
import books
import blog
import helper
import comments

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'mainpage.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

class AccessDenied(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'accessdenied.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

class NotFound(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'notfound.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

class SaveYourLoluser(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'saveyourloluser.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

application = webapp.WSGIApplication([
        ('/', MainPage),

        (r'/books/([\d\w_]+)', books.ViewBooks),
        ('/editbook', books.EditBook),
        ('/deletebook', books.DeleteBook),
        ('/savebook', books.SaveBook),

        (r'/loluser/([\d\w_]+)', loluser.ViewLoluser),
        ('/saveloluser', loluser.SaveLoluser),

        (r'/blog/([\d\w_]+)', blog.ViewBlog),
        ('/editpost', blog.EditPost),
        ('/deletepost', blog.DeletePost),
        ('/savepost', blog.SavePost),
        (r'/blog/([\d\w_]+)/([\d\w_]+)', blog.ViewPost),

        ('/savecomment', comments.SaveComment),
        ('/replytocomment', comments.ReplyToComment),

        ('/notfound', NotFound),
        ('/accessdenied', AccessDenied),
        ('/saveyourloluser', SaveYourLoluser),
        (r'/.*', NotFound),
        ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
