from google.appengine.ext import db
from google.appengine.api import users
import os

def values(uri):
    user = users.get_current_user()
    profile = None
    if user:
        profile = db.GqlQuery('select * from Profile where userid = :1', user.user_id()).get()
    values = {
        'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
        'login_url' : users.create_login_url(uri),
        'logout_url' : users.create_logout_url(uri),
        'user' : user,
        'profile' : profile
        }
    return values

def profile(userid):
    return db.GqlQuery('select * from Profile where userid = :1', userid).get()

def check_for_profile(handler):
    user = users.get_current_user()
    if not user:
        handler.redirect(users.create_login_url(handler.request.uri))
        return False
    prof = profile(user.user_id())
    if not prof:
        handler.redirect('/saveyourprofile')
        return False
    return True
