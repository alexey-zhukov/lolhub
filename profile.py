from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import blog
import helper

class Profile(db.Model):
    id = db.IntegerProperty()
    user = db.UserProperty()
    userid = db.StringProperty()

class ViewProfile(webapp.RequestHandler):
    def get(self, userid):
        profile = helper.profile(userid)
        if not profile:
            self.redirect('/notfound')
        else:
            values = { 'owner' : profile }
            values.update(helper.values(self.request.uri))
            path = os.path.join(os.path.dirname(__file__), 'profile.html')
            self.response.out.write(template.render(path, values))

class SaveProfile(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (not user):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            profile = helper.profile_by_google_user_id(user.user_id())
            if (not profile):
                profile = Profile()
                profile.userid = user.user_id()
                profile.user = user
                maxProfile = Profile.all().order("-id").get()
                if not maxProfile or not maxProfile.id:
                    profile.id = 1
                else:
                    profile.id = maxProfile.id + 1
                profile.put()
            self.redirect('/')
