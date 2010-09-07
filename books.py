from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
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
            except ValueError:
                book.total_pages = 0
            try:
                book.current_page = int(self.request.get("current_page"))
            except ValueError:
                book.current_page = 0
            try:
                book.year = int(self.request.get("year"))
            except ValueError:
                book.year = 0
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

def main():
    pass

if __name__ == "__main__":
    main()
