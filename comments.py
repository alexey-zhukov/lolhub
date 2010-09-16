from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.db import BadKeyError
import os

import loluser
import blog
import helper

class Comment(db.Model):
    id = db.IntegerProperty()
    author = db.ReferenceProperty(loluser.Loluser)
    post = db.ReferenceProperty(blog.Post)
    parent_comment = db.SelfReferenceProperty()
    content = db.TextProperty()
    date_posted = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)
    def depth(self):
        if self.parent_comment:
            return self.parent_comment.depth() + 1
        else:
            return 0
    def depth_margin(self):
        return min(12 + 2*self.depth(), 70)
    def width(self):
        return 90-self.depth_margin()

class SaveComment(webapp.RequestHandler):
    def post(self):
        if users.get_current_user():
            loluser = helper.loluser_by_google_user_id(users.get_current_user().user_id())
        else:
            loluser = None
        #if self.request.get('key'):
        #    try:        
        #        comment = db.get(db.Key(self.request.get("key")))
        #    except BadKeyError:
        #        self.redirect('/notfound')
        #        return
        #    if not helper.check_for_existence_and_ownership2(comment, self): return
        #else:
        comment = Comment()
        comment.author = loluser
        comment.depth = 0
        maxComment = Comment.all().order("-id").get()
        if not maxComment or not maxComment.id:
            comment.id = 1
        else:
            comment.id = maxComment.id + 1
        comment.content = self.request.get("content")
        try:
            parent_comment = db.get(db.Key(self.request.get("parent_comment")))
        except BadKeyError:
            parent_comment = None
        comment.parent_comment = parent_comment
        post = db.get(db.Key(self.request.get("post")))
        comment.post = post
        comment.put()
        self.redirect("/blog/" + str(post.userid) + "/" + str(post.id))

class ReplyToComment(webapp.RequestHandler):
    def get(self):
        comment = db.get(db.Key(self.request.get("comment")))
        values = { 'comment' : comment }
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'replytocomment.html')
        self.response.out.write(template.render(path, values))
