from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

import books
import profile

class MainPage(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            books = db.GqlQuery('select * from Book where user = :1 order by' +
                                ' date_edited desc',
                                users.get_current_user())
            logout_url = users.create_logout_url(self.request.uri)
            values = {
                'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
                'login_url' : users.create_login_url(self.request.uri),
                'logout_url' : users.create_logout_url(self.request.uri),
                'user' : users.get_current_user(),
                'books' : books,
                }
            path = os.path.join(os.path.dirname(__file__), 'books.html')
            self.response.out.write(template.render(path, values))

class AccessDenied(webapp.RequestHandler):
    def get(self):
        values = {
            'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
            'login_url' : users.create_login_url(self.request.uri),
            'logout_url' : users.create_logout_url(self.request.uri),
            'user' : users.get_current_user(),
            }
        path = os.path.join(os.path.dirname(__file__), 'accessdenied.html')
        self.response.out.write(template.render(path, values))

class NotFound(webapp.RequestHandler):
    def get(self):
        values = {
            'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
            'login_url' : users.create_login_url(self.request.uri),
            'logout_url' : users.create_logout_url(self.request.uri),
            'user' : users.get_current_user(),
            }
        path = os.path.join(os.path.dirname(__file__), 'notfound.html')
        self.response.out.write(template.render(path, values))

application = webapp.WSGIApplication([
        ("/", MainPage),
        ("/addbook", books.AddBook),
        ("/editbook", books.EditBook),
        ("/savebook", books.SaveBook),
        ("/accessdenied", AccessDenied),
        ("/notfound", NotFound),
        ("/delete", books.DeleteBook),
        (r'/profile/(.*)', profile.ShowProfile),
        ("/editprofile", profile.EditProfile),
        ("/saveprofile", profile.SaveProfile),
        ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
