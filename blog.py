from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import helper

class Post(db.Model):
    userid = db.StringProperty()
    title = db.StringProperty()
    content = db.StringProperty()
    date_posted = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)

class ViewBlog(webapp.RequestHandler):
    def get(self, userid):
        profile = helper.profile(userid)
        if not profile:
            self.redirect('/notfound')
            return
        posts = db.GqlQuery('select * from Post where userid = :1 order by' +
                            ' date_posted desc',
                            userid)
        values = { 'posts' : posts, 'owner' : profile.user }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, values))

class EditPost(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            post = db.get(db.Key(self.request.get("key")))
            if not post:
                self.redirect("/notfound")
                return
            if post.userid != user.user_id():
                self.redirect("/accessdenied")
                return
            values = { 'post' : post }
        else:
            values = {}
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'editpost.html')
        self.response.out.write(template.render(path, values))

class SavePost(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            post = db.get(db.Key(self.request.get("key")))
            if not post:
                self.redirect("/notfound")
                return
            if post.userid != user.user_id():
                self.redirect("/accessdenied")
                return
        else:
            post = Post()
            post.userid = user.user_id()
        post.title = self.request.get("title")
        post.content = self.request.get("content")
        post.put()
        self.redirect("/blog/" + user.user_id())
                        
class DeletePost(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not helper.check_for_profile(self):
            return
        post = db.get(db.Key(self.request.get("key")))
        if (post.userid != user.user_id()):
            self.redirect("/accessdenied")
            return
        post.delete()
        self.redirect("/blog/" + user.user_id())

def main():
    pass

if __name__ == "__main__":
    main()
