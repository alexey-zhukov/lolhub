from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import blog
import helper

class Loluser(db.Model):
    id = db.IntegerProperty()
    user = db.UserProperty()
    userid = db.StringProperty()
    nickname = db.StringProperty()
    def nickname_wrap(self):
        if self.nickname:
            return self.nickname
        return "hidden user"

class ViewLoluser(webapp.RequestHandler):
    def get(self, userid):
        loluser = helper.loluser(userid)
        if not loluser:
            self.redirect('/notfound')
        else:
            values = { 'owner' : loluser }
            values.update(helper.values(self.request.uri))
            path = os.path.join(os.path.dirname(__file__), 'loluser.html')
            self.response.out.write(template.render(path, values))

class SaveNickname(webapp.RequestHandler):
    def valid(self, nickname):
        if ' ' in nickname:
            return 'no spaces'
        if len(nickname) < 2:
            return 'minimum length = 2'
        if len(nickname) > 42:
            return 'maximum length = 42'
        existing = db.GqlQuery('select * from Loluser where nickname = :1', nickname).get()
        if existing:
            return 'already exists'
        return 'valid'

    def post(self):
        user = users.get_current_user()
        if (not user):
            self.redirect(users.create_login_url(self.request.uri))
            return
        nickname = self.request.get("nickname")
        if not self.valid(nickname) == 'valid':
            values = { 'error' : self.valid(nickname), 'nickname' : nickname }
            values.update(helper.values(self.request.uri))
            path = os.path.join(os.path.dirname(__file__), 'saveloluser.html')
            self.response.out.write(template.render(path, values))
            return

        loluser = helper.loluser_by_google_user_id(user.user_id())
        if (not loluser):
            loluser = Loluser()
            loluser.userid = user.user_id()
            loluser.user = user
            maxLoluser = Loluser.all().order("-id").get()
            if not maxLoluser or not maxLoluser.id:
                loluser.id = 1
            else:
                loluser.id = maxLoluser.id + 1
        loluser.nickname = nickname
        loluser.put()
        self.redirect('/')

class SaveLoluser(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (not user):
            self.redirect(users.create_login_url(self.request.uri))
            return
        path = os.path.join(os.path.dirname(__file__), 'saveloluser.html')
        self.response.out.write(template.render(path, helper.values(self.request.uri)))

def main():
    pass

if __name__ == "__main__":
    main()
