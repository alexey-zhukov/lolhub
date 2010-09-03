from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

class Book(db.Model):
    user = db.UserProperty()
    author = db.StringProperty()
    title = db.StringProperty()
    total_pages = db.IntegerProperty()
    year = db.IntegerProperty()
    current_page = db.IntegerProperty()
    date_added = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)

class MainPage(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            books = db.GqlQuery("select * from Book where user = :1 order by date_edited desc",
                                users.get_current_user())
            logout_url = users.create_logout_url(self.request.uri)
            values = { 'books' : books, 'logout_url' : logout_url,
                       'nickname' : users.get_current_user().nickname() }
            path = os.path.join(os.path.dirname(__file__), 'books.html')
            self.response.out.write(template.render(path, values))

class AddBook(webapp.RequestHandler):
    def post(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            book = Book()
            book.user = users.get_current_user()
            book.author = self.request.get("author")
            book.title = self.request.get("title")
            try:
                book.total_pages = int(self.request.get("total_pages"))
            except ValueError: book.total_pages = 0
            try:
                book.current_page = int(self.request.get("current_page"))
            except ValueError: book.current_page = 0
            try:
                book.year = int(self.request.get("year"))
            except ValueError: book.year = 0
            book.put()
            self.redirect("/")

class EditBook(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            book = db.get(db.Key(self.request.get("key")))
            logout_url = users.create_logout_url(self.request.uri)
            values = { 'book' : book, 'logout_url' : logout_url }
            path = os.path.join(os.path.dirname(__file__), 'editbook.html')
            self.response.out.write(template.render(path, values))

class SaveBook(webapp.RequestHandler):
    def post(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            book = db.get(db.Key(self.request.get("key")))
            if (book.user != users.get_current_user()):
                self.redirect("/accessdenied")
            else:
                book.author = self.request.get("author")
                book.title = self.request.get("title")
                try:
                    book.total_pages = int(self.request.get("total_pages"))
                except ValueError: pass
                try:
                    book.current_page = int(self.request.get("current_page"))
                except ValueError: pass
                try:
                    book.year = int(self.request.get("year"))
                except ValueError: pass
                book.put()
                self.redirect("/")

class DeleteBook(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            book = db.get(db.Key(self.request.get("key")))
            if (book.user != users.get_current_user()):
                self.redirect("/accessdenied")
            else:
                book.delete()
                self.redirect("/")

class AccessDenied(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'accessdenied.html')
        self.response.out.write(template.render(path, {}))

application = webapp.WSGIApplication([
        ("/", MainPage),
        ("/addbook", AddBook),
        ("/editbook", EditBook),
        ("/savebook", SaveBook),
        ("/accessdenied", AccessDenied),
        ("/delete", DeleteBook),
        ], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
