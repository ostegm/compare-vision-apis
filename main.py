"""The main python server which routes requests from the fontend to vapis."""
import logging
import os
import json
import jinja2
import webapp2
from clarifai.rest import ClarifaiApp
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
  image_data = {
      "image": {"source": {"imageUri": url}},
      "features": [{"type": "LABEL_DETECTION"}]
  }
  data = {"requests": [image_data]}
  return json.dumps(data)


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
    """Responds to post request with clarifai prediction/"""
    clarifai_key = Settings.get('CLARIFAI_API_KEY')
    clarifai_app = ClarifaiApp(api_key=clarifai_key)
    model = clarifai_app.models.get("general-v1.3")
    image_url = self.request.get('image_url')
    prediction = model.predict_by_url(url=image_url)
    logging.info('Prediction from clarifai app: %s', prediction)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write(prediction)


class GoogleWrapper(webapp2.RequestHandler):
  """Wrapper class to send an image classification request to Google."""

  def post(self):
    """Responds to post request with Google Vision API prediction"""
    google_key = Settings.get('GOOGLE_API_KEY')
    headers = {
        'Content-Type': 'application/json',
    }
    image_url = self.request.get('image_url')
    data = make_google_data(image_url)
    url = 'https://vision.googleapis.com/v1/images:annotate?key=' + google_key
    response = requests.post(url, data=data, headers=headers)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write(response.content)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/clarifai', ClarifaiWrapper),
    ('/google', GoogleWrapper)
], debug=True)
