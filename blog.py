from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

class Post(db.Model):
    user = db.UserProperty()
    title = db.StringProperty()
    content = db.StringProperty()
    date_posted = db.DateTimeProperty(auto_now_add = True)
    date_edited = db.DateTimeProperty(auto_now = True)
