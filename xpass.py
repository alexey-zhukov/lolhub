from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import helper

class Xpass(webapp.RequestHandler):
    def get(self):
        if not users.is_current_user_admin():
            self.redirect("/accessdenied")
            return
        values = {}
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'html/xpass.html')
        self.response.out.write(template.render(path, values))

def main():
    pass

if __name__ == "__main__":
    main()
