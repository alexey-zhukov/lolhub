from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os

import helper

class Js1(webapp.RequestHandler):
    def get(self):
        values = {}
        values.update(helper.values(self.request.uri))
        path = os.path.join(os.path.dirname(__file__), 'html/js1.html')
        self.response.out.write(template.render(path, values))
