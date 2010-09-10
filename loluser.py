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

class SaveLoluser(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (not user):
            self.redirect(users.create_login_url(self.request.uri))
        else:
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
                loluser.put()
            self.redirect('/')

def main():
    pass

if __name__ == "__main__":
    main()
