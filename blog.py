from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.db import BadKeyError
import os
import re

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
    def comment_count(self):
        return db.GqlQuery('select * from Comment where post = :1', self).count()

class ViewBlog(webapp.RequestHandler):
    def get(self, userid):
        loluser = helper.loluser(userid)
        if not loluser:
            self.redirect('/notfound')
            return
        if (self.request.get('page')):
            try:
                intpage = int(self.request.get('page'))
            except ValueError:
                self.redirect('/notfound')
                return
        else:
            intpage = 0
        posts_per_page = 5
        total_posts = db.GqlQuery('select * from Post where userid = :1 order by' +
                                  ' date_posted desc',
                                  int(userid)).count()
        posts = db.GqlQuery('select * from Post where userid = :1 order by' +
                            ' date_posted desc limit ' + str(posts_per_page) + ' offset '
                            + str(intpage*posts_per_page),
                            int(userid))
        nextpage = intpage+1
        prevpage = intpage-1
        if total_posts <= intpage*posts_per_page + posts_per_page:
            nextpage = -1
        values = { 'posts' : posts, 'owner' : loluser, 'page' : str(intpage),
                   'nextpage' : str(nextpage), 'prevpage' : str(prevpage) }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, values))

class TempComment:
    me = None
    children = []

class ViewPost(webapp.RequestHandler):
    def append_all(self, tmp, list):
        list.append(tmp.me)
        for child in tmp.children:
            self.append_all(child, list)

    def get(self, userid, postid):
        loluser = helper.loluser(userid)
        if not loluser:
            self.redirect('/notfound')
            return
        post = Post.gql('where id = :1', int(postid)).get()
        if not post or post.userid != loluser.id:
            self.redirect('/notfound')
            return

        comments = db.GqlQuery('select * from Comment where post = :1 order by' +
                               ' date_posted asc',
                               post)
        root = TempComment()
        root.children = []
        hm = {}
        for comment in comments:
            tmp = TempComment()
            tmp.me = comment
            tmp.children = []
            if comment.parent_comment:
                par = hm[comment.parent_comment.id]
            else:
                par = root
            hm[comment.id] = tmp
            par.children.append(tmp)
        #for child in root.children:
        #    print child.children

        comments = []
        for child in root.children:
            self.append_all(child, comments)
        values = { 'post' : post, 'owner' : loluser, 'comments' : comments }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'post.html')
        self.response.out.write(template.render(path, values))

class EditPost(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        loluser = helper.loluser_by_google_user_id(user.user_id())
        if not helper.check_for_loluser(self): return
        if self.request.get('key'):
            try:
                post = db.get(db.Key(self.request.get("key")))
            except BadKeyError:
                self.redirect('/notfound')
                return
            if not helper.check_for_existence_and_ownership(post, self): return
            values = { 'post' : post }
        else:
            values = {}
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'editpost.html')
        self.response.out.write(template.render(path, values))

class SavePost(webapp.RequestHandler):
    def get(self):
        self.redirect('/notfound')

    def post(self):
        loluser = helper.loluser_by_google_user_id(users.get_current_user().user_id())
        if not helper.check_for_loluser(self): return
        if self.request.get('key'):
            try:        
                post = db.get(db.Key(self.request.get("key")))
            except BadKeyError:
                self.redirect('/notfound')
                return
            if not helper.check_for_existence_and_ownership(post, self): return
        else:
            post = Post()
            post.userid = loluser.id
            maxPost = Post.all().order("-id").get()
            if not maxPost or not maxPost.id:
                post.id = 1
            else:
                post.id = maxPost.id + 1
        post.title = self.request.get("title")
        post.content = self.request.get("content")
        post.put()
        self.redirect("/blog/" + str(loluser.id))
                        
class DeletePost(webapp.RequestHandler):
    def get(self):
        loluser = helper.loluser_by_google_user_id(users.get_current_user().user_id())
        if not helper.check_for_loluser(self): return
        try:        
            post = db.get(db.Key(self.request.get("key")))
        except BadKeyError:
            self.redirect('/notfound')
            return
        if not helper.check_for_existence_and_ownership(post, self): return
        post.delete()
        self.redirect("/blog/" + str(loluser.id))

def main():
    pass

if __name__ == "__main__":
    main()
