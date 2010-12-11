from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class DeadlyStuff(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'html/ds.html')
        self.response.out.write(template.render(path, {}))

def main():
    pass

if __name__ == "__main__":
    main()
