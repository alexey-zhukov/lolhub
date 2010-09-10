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
        'google_user' : user,
        'user' : profile,
        }
    return values

def profile(userid):
    return db.GqlQuery('select * from Profile where id = :1', int(userid)).get()

def profile_by_google_user_id(userid):
    return db.GqlQuery('select * from Profile where userid = :1', userid).get()

def check_for_profile(handler):
    user = users.get_current_user()
    if not user:
        handler.redirect(users.create_login_url(handler.request.uri))
        return False
    prof = profile_by_google_user_id(user.user_id())
    if not prof:
        handler.redirect('/saveyourprofile')
        return False
    return True

def check_for_existence_and_ownership(entity, handler):
    user = users.get_current_user()
    profile = profile_by_google_user_id(user.user_id())
    if not entity:
        handler.redirect("/notfound")
        return False
    if (entity.userid != profile.id):
        handler.redirect("/accessdenied")
        return False
    return True

def main():
    pass

if __name__ == "__main__":
    main()
