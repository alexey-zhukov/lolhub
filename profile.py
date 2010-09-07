from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

class Profile(db.Model):
    user = db.UserProperty()
    username = db.StringProperty()

class ShowProfile(webapp.RequestHandler):
    def get(self, username):
        found_users = db.GqlQuery('select * from Profile where username = :1', username)
        if (found_users.count() == 0):
            self.redirect('/notfound')
        else:
            if (users.get_current_user() == None):
                nickname = None
            else:
                nickname = users.get_current_user().nickname()
            values = { 'nickname' : nickname, 'username' : username }
            path = os.path.join(os.path.dirname(__file__), 'profile.html')
            self.response.out.write(template.render(path, values))

class EditProfile(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            found_profiles = db.GqlQuery('select * from Profile where user = :1', users.get_current_user())
            if (found_profiles.count() > 0):
                profile = found_profiles[0]
            else:
                profile = None
            logout_url = users.create_logout_url(self.request.uri)
            values = { 'profile' : profile,
                       'user' : users.get_current_user(),
                       'logout_url' : logout_url,
                       }
            path = os.path.join(os.path.dirname(__file__), 'editprofile.html')
            self.response.out.write(template.render(path, values))

class SaveProfile(webapp.RequestHandler):
    def post(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            found_profiles = db.GqlQuery('select * from Profile where user = :1', users.get_current_user())
            profile = found_profiles.get()
            if (profile != None and profile.user != users.get_current_user()):
                self.redirect('/accessdenied')
            else:
                if (profile == None and (self.request.get('username') == None
                                         or self.request.get('username').length == 0)):
                    self.redirect('/')
                else:
                    if (profile == None):
                        profile = Profile()
                        profile.user = users.get_current_user()
                        profile.username = self.request.get('username')
                    profile.put()
                    self.redirect('/')
