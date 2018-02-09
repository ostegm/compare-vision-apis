import logging
import os
import urllib
import jinja2
import webapp2
import json
# from clarifai.rest import ClarifaiApp
from google.appengine.ext import ndb
import requests
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
    NOT_SET_VALUE = "NOT SET"
    retval = Settings.query(Settings.name == name).get()
    if not retval:
      retval = Settings()
      retval.name = name
      retval.value = NOT_SET_VALUE
      retval.put()
    if retval.value == NOT_SET_VALUE:
      raise Exception(('Setting %s not found in the database. A placeholder ' +
        'record has been created. Go to the Developers Console for your app ' +
        'in App Engine, look up the Settings record with name=%s and enter ' +
        'its value in that record\'s value field.') % (name, name))
    return retval.value


class MainPage(webapp2.RequestHandler):

  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render())


class ClarifaiWrapper(webapp2.RequestHandler):

  def post(self):
    # logging.info('Starting post request handler.')
    # CLARIFAI_KEY = Settings.get('CLARIFAI_API_KEY')
    # # model = clarifai_app.models.get("general-v1.3")
    # # logging.info('CLARIFAI Models instatiated.')
    image_url = self.request.get('image_url')
    image_category = self.request.get('image_category')

    # prediction = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Key be333133d4e444dea5545f60c06bea89',
    }
    data = json.dumps({
       "inputs": [
         {
           "data": {
             "image": {
               "url": "https://samples.clarifai.com/metro-north.jpg"
             }
           }
         }
       ]
     })
    logging.info(data)
    c_url = 'https://api.clarifai.com/v2/models/aaa03c23b3724a16a56b629203edc62c/outputs'
    response = requests.post(c_url, data=data, headers=headers)
    logging.info('Prediction: \n%s', response.content)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("you sent: " + response.content)


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/clarifai', ClarifaiWrapper),
], debug=True)