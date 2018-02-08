import logging
import os
import urllib
import jinja2
import webapp2
from clarifai.rest import ClarifaiApp
from google.appengine.ext import ndb


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
    CLARIFAI_KEY = Settings.get('CLARIFAI_API_KEY')
    # clarifai_app = ClarifaiApp(api_key=CLARIFAI_API_KEY)
    # model = clarifai_app.models.get("general-v1.3")

    image_url = self.request.get('image_url')
    image_category = self.request.get('image_category')

    # predict with the model
    # prediction = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
    # logging.info('Prediction: \n%s', prediction)
    # Output response of application-3 to screen
    logging.info('Request incoming: %s', self.request)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write("you sent: " + image_category)


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/clarifai', ClarifaiWrapper),
], debug=True)