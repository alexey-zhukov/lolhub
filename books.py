from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import helper

class Book(db.Model):
    userid = db.StringProperty()
    author = db.StringProperty()
    title = db.StringProperty()
    total_pages = db.IntegerProperty()
    year = db.IntegerProperty()
    current_page = db.IntegerProperty()
    date_added = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)

class ViewBooks(webapp.RequestHandler):
    def get(self, userid):
        profile = helper.profile(userid)
        if not profile:
            self.redirect('/notfound')
            return
        books = db.GqlQuery('select * from Book where userid = :1 order by' +
                            ' date_edited desc',
                            userid)
        values = { 'books' : books, 'owner' : profile.user }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'books.html')
        self.response.out.write(template.render(path, values))

class EditBook(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            book = db.get(db.Key(self.request.get("key")))
            if not book:
                self.redirect("/notfound")
                return
            if book.userid != user.user_id():
                self.redirect("/accessdenied")
                return
            values = { 'book' : book }
        else:
            values = {}
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'editbook.html')
        self.response.out.write(template.render(path, values))

class SaveBook(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            book = db.get(db.Key(self.request.get("key")))
            if not book:
                self.redirect("/notfound")
                return
            if book.userid != user.user_id():
                self.redirect("/accessdenied")
                return
        else:
            book = Book()
            book.userid = user.user_id()
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
        self.redirect("/books/" + user.user_id())
                        
class DeleteBook(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        book = db.get(db.Key(self.request.get("key")))
        if (book.userid != user.user_id()):
            self.redirect("/accessdenied")
            return
        book.delete()
        self.redirect("/books/" + user.user_id())

def main():
    pass

if __name__ == "__main__":
    main()
