from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

import books
import profile
import helper

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'mainpage.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))
        #if (users.get_current_user() == None):
        #    self.redirect(users.create_login_url(self.request.uri))
        #else:
        #    books = db.GqlQuery('select * from Book where userid = :1 order by' +
        #                        ' date_edited desc',
        #                        users.get_current_user().user_id())
        #    logout_url = users.create_logout_url(self.request.uri)
        #    values = { 'books' : books }
        #    values.update(helper.values(self.request.uri))
        #    path = os.path.join(os.path.dirname(__file__), 'books.html')
        #    self.response.out.write(template.render(path, values))

class AccessDenied(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'accessdenied.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

class NotFound(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'notfound.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

application = webapp.WSGIApplication([
        ("/", MainPage),
        (r'/books/([\d\w]+)', books.ViewBooks),

        ("/notfound", NotFound),
        ("/accessdenied", AccessDenied),

        ("/addbook", books.AddBook),
        ("/editbook", books.EditBook),
        ("/savebook", books.SaveBook),
        ("/delete", books.DeleteBook),
        (r'/profile/(.*)', profile.ShowProfile),
        ("/editprofile", profile.EditProfile),
        ("/saveprofile", profile.SaveProfile),
        ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
