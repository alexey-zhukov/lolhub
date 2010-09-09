from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.db import BadKeyError
import os

import helper

class Post(db.Model):
    id = db.IntegerProperty()
    userid = db.IntegerProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    date_posted = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)
    def preview_full(self):
        return len(self.content) <= 500
    def content_preview(self):
        return  self.content[:500]
    def date_posted_formatted(self):
        return self.date_posted.strftime("%d.%m.%Y %H:%M")

class ViewBlog(webapp.RequestHandler):
    def get(self, userid):
        profile = helper.profile(userid)
        if not profile:
            self.redirect('/notfound')
            return
        posts = db.GqlQuery('select * from Post where userid = :1 order by' +
                            ' date_posted desc',
                            int(userid))
        values = { 'posts' : posts, 'owner' : profile }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, values))

class ViewPost(webapp.RequestHandler):
    def get(self, userid, postid):
        profile = helper.profile(userid)
        if not profile:
            self.redirect('/notfound')
            return
        post = Post.gql('where id = :1', int(postid)).get()
        if not post or post.userid != profile.id:
            self.redirect('/notfound')
            return
        values = { 'post' : post, 'owner' : profile }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'post.html')
        self.response.out.write(template.render(path, values))

class EditPost(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        profile = helper.profile_by_google_user_id(user.user_id())
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            post = db.get(db.Key(self.request.get("key")))
            if not post:
                self.redirect("/notfound")
                return
            if post.userid != profile.id:
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
        profile = helper.profile_by_google_user_id(user.user_id())
        if not helper.check_for_profile(self):
            return
        if self.request.get('key'):
            try:        
                post = db.get(db.Key(self.request.get("key")))
            except BadKeyError:
                self.redirect('/notfound')
                return
            if not helper.check_for_existence_and_ownership(post, self): return
        else:
            post = Post()
            post.userid = profile.id
            maxPost = Post.all().order("-id").get()
            if not maxPost or not maxPost.id:
                post.id = 1
            else:
                post.id = maxPost.id + 1
        post.title = self.request.get("title")
        post.content = self.request.get("content")
        post.put()
        self.redirect("/blog/" + str(profile.id))
                        
class DeletePost(webapp.RequestHandler):
    def get(self):
        profile = helper.profile_by_google_user_id(users.get_current_user().user_id())
        if not helper.check_for_profile(self): return
        try:        
            post = db.get(db.Key(self.request.get("key")))
        except BadKeyError:
            self.redirect('/notfound')
            return
        if not helper.check_for_existence_and_ownership(post, self): return
        post.delete()
        self.redirect("/blog/" + str(profile.id))

def main():
    pass

if __name__ == "__main__":
    main()
