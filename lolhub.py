from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

import books
import profile
import helper
import blog

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

class SaveYourProfile(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'saveyourprofile.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

application = webapp.WSGIApplication([
        ('/', MainPage),

        (r'/books/([\d\w_]+)', books.ViewBooks),
        ('/editbook', books.EditBook),
        ('/deletebook', books.DeleteBook),
        ('/savebook', books.SaveBook),

        (r'/profile/([\d\w_]+)', profile.ViewProfile),
        ('/saveprofile', profile.SaveProfile),

        (r'/blog/([\d\w_]+)', blog.ViewBlog),
        ('/editpost', blog.EditPost),
        ('/deletepost', blog.DeletePost),
        ('/savepost', blog.SavePost),
        (r'/blog/([\d\w_]+)/([\d\w_]+)', blog.ViewPost),

        ('/notfound', NotFound),
        ('/accessdenied', AccessDenied),
        ('/saveyourprofile', SaveYourProfile),
        (r'/.*', NotFound),
        ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
