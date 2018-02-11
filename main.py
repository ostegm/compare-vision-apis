"""The main python server which routes requests from the fontend to vapis."""
import logging
import os
import jinja2
import webapp2
from clarifai.rest import ClarifaiApp
from google.appengine.ext import ndb
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Settings(ndb.Model):
  """Helper class to get or set values in datastore."""
  name = ndb.StringProperty()
  value = ndb.StringProperty()

  @staticmethod
  def get(name):
    """Checks for key in db, if present returns the value, otherwise alerts."""
    not_set_value = "NOT SET"
    retval = Settings.query(Settings.name == name).get()
    if not retval:
      retval = Settings()
      retval.name = name
      retval.value = not_set_value
      retval.put()
    if retval.value == not_set_value:
      raise Exception(
          'Setting %s not found in the database. Use the app engine developer' +
          'console and add a value.' %(name)
      )
    return retval.value


class MainPage(webapp2.RequestHandler):
  """Renders the main page template."""

  def get(self):
    """Loads and shows the main page."""
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())


class ClarifaiWrapper(webapp2.RequestHandler):

  def post(self):
    """Responds to post request with clarifai prediction"""
    logging.info('Request: %s', self.request)
    clarifai_key = Settings.get('CLARIFAI_API_KEY')
    clarifai_app = ClarifaiApp(api_key=clarifai_key)
    model = clarifai_app.models.get("general-v1.3")
    image_url = self.request.get('image_url')
    image_category = self.request.get('image_category')
    prediction = model.predict_by_url(url=image_url)
    logging.info('Prediction from clarifai app: %s', prediction)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("Clarifai app prediction: " + str(prediction))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/clarifai', ClarifaiWrapper),
], debug=True)
