from google.appengine.ext import db
from google.appengine.api import users
import os

def values(uri):
    user = users.get_current_user()
    lol = None
    if user:
        lol = db.GqlQuery('select * from Loluser where userid = :1', user.user_id()).get()
    values = {
        'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
        'login_url' : users.create_login_url(uri),
        'logout_url' : users.create_logout_url(uri),
        'google_user' : user,
        'loluser' : lol,
        }
    return values

def loluser(userid):
    return db.GqlQuery('select * from Loluser where id = :1', int(userid)).get()

def loluser_by_google_user_id(userid):
    return db.GqlQuery('select * from Loluser where userid = :1', userid).get()

def check_for_loluser(handler):
    user = users.get_current_user()
    if not user:
        handler.redirect(users.create_login_url(handler.request.uri))
        return False
    lol = loluser_by_google_user_id(user.user_id())
    if not lol:
        handler.redirect('/saveyourloluser')
        return False
    return True

def check_for_existence_and_ownership(entity, handler):
    user = users.get_current_user()
    lol = loluser_by_google_user_id(user.user_id())
    if not entity:
        handler.redirect("/notfound")
        return False
    if (entity.userid != lol.id):
        handler.redirect("/accessdenied")
        return False
    return True

def check_for_existence_and_ownership2(entity, handler):
    user = users.get_current_user()
    lol = loluser_by_google_user_id(user.user_id())
    if not entity:
        handler.redirect("/notfound")
        return False
    if (entity.author != lol):
        handler.redirect("/accessdenied")
        return False
    return True


def main():
    pass

if __name__ == "__main__":
    main()
