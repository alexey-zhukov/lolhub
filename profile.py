from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import blog

class Profile(db.Model):
    userid = db.StringProperty()
    username = db.StringProperty()

class ShowProfile(webapp.RequestHandler):
    def get(self, userid):
        found_profile = db.GqlQuery('select * from Profile where userid = :1', userid)
        if (found_profile.count() == 0):
            self.redirect('/notfound')
        else:
            if (users.get_current_user() == None):
                nickname = None
            else:
                nickname = users.get_current_user().nickname()
            prof = found_profile.get()
            books = db.GqlQuery('select * from Book where userid = :1 order by' +
                                ' date_edited desc limit 4',
                                prof.userid)
            posts = db.GqlQuery('select * from Post where user = :1 order by' +
                                ' date_posted desc limit 4',
                                prof.user)
            values = {
                'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
                'login_url' : users.create_login_url(self.request.uri),
                'logout_url' : users.create_logout_url(self.request.uri),
                'user' : users.get_current_user(),
                'nickname' : nickname,
                'username' : username,
                'books' : books,
                'posts' : posts,
                }
            path = os.path.join(os.path.dirname(__file__), 'profile.html')
            self.response.out.write(template.render(path, values))

class EditProfile(webapp.RequestHandler):
    def get(self):
        if (users.get_current_user() == None):
            self.redirect(users.create_login_url(self.request.uri))
        else:
            found_profiles = db.GqlQuery('select * from Profile where user = :1', users.get_current_user())
            if (found_profiles.count() > 0):
                prof = found_profiles.get()
            else:
                prof = None
            logout_url = users.create_logout_url(self.request.uri)
            values = {
                'toolbar' : os.path.join(os.path.dirname(__file__), 'toolbar.html'),
                'login_url' : users.create_login_url(self.request.uri),
                'logout_url' : users.create_logout_url(self.request.uri),
                'user' : users.get_current_user(),
                'profile' : prof,
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
                                         or len(self.request.get('username')) == 0)):
                    self.redirect('/')
                else:
                    if (profile == None):
                        profile = Profile()
                        profile.user = users.get_current_user()
                        profile.username = self.request.get('username')
                    profile.put()
                    self.redirect('/')
