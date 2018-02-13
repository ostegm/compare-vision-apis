"""The main python server which routes requests from the fontend to vapis."""
import logging
import os
import json
import jinja2
import webapp2
from google.appengine.ext import ndb
import requests
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def make_google_data(url):
  """Constructs the data object for a post request to Google Vision API."""
  headers = {'Content-Type': 'application/json'}
  image_data = {
      "image": {"source": {"imageUri": url}},
      "features": [{"type": "LABEL_DETECTION"}]
  }
  data = {"requests": [image_data]}
  return headers, json.dumps(data)

def make_clarifai_data(url, auth_key):
  """Constructs the data object for a post request to Clarifai."""
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Key {}'.format(auth_key)
  }
  data = {"inputs": [{"data": {"image": {"url": url}}}]}
  return headers, json.dumps(data)


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
          'Setting %s not found in the database.' %(name) +
          'Use the app engine developer console and add a value.'
      )
    return retval.value


class MainPage(webapp2.RequestHandler):
  """Renders the main page template."""

  def get(self):
    """Loads and shows the main page."""
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())


class ClarifaiWrapper(webapp2.RequestHandler):
  """Wrapper class to send post request to Clarifai vision api."""

  def post(self):
    clarifai_key = Settings.get('CLARIFAI_API_KEY')
    image_url = self.request.get('imageUrl')
    headers, data = make_clarifai_data(image_url, clarifai_key)
    url = 'https://api.clarifai.com/v2/models/aaa03c23b3724a16a56b629203edc62c/outputs'
    response = requests.post(url, data=data, headers=headers)
    logging.info('Prediction from clarifai: %s', response.content)
    self.response.headers['Content-Type'] = 'text/json'
    self.response.write(response.content)

class GoogleWrapper(webapp2.RequestHandler):
  """Wrapper class to send an image classification request to Google."""

  def post(self):
    """Responds to post request with Google Vision API prediction"""
    google_key = Settings.get('GOOGLE_API_KEY')
    image_url = self.request.get('imageUrl')
    headers, data = make_google_data(image_url)
    url = 'https://vision.googleapis.com/v1/images:annotate?key=' + google_key
    response = requests.post(url, data=data, headers=headers)
    logging.info('Prediction from google vision: %s', response.content)
    self.response.headers['Content-Type'] = 'text/json'
    self.response.write(response.content)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/clarifai', ClarifaiWrapper),
    ('/google', GoogleWrapper)
], debug=True)
