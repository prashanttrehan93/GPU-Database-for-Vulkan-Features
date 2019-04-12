import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class Compare(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login/logout link
        # and also a string to show this
		url = ''
		url_string = ''
		welcome = 'Welcome back'

		# pulling back the current user from the request
		user = users.get_current_user()

		if user:
			url = users.create_logout_url("/")
			url_string = 'logout'

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		name = self.request.get('name')
		mygpu_key = ndb.Key('MyGpu',name)
		mygpu = mygpu_key.get()

		if mygpu is None:
			self.redirect("/")

		template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
			'gpu_array' : MyGpu.query().fetch(),
			'mygpu' : mygpu
		}

        # pull the template file and asking jinja to render
        # Now it will be given template values
		template = JINJA_ENVIRONMENT.get_template('compare.html')
		self.response.write(template.render(template_values))


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		# This is URL that will contain a login/logout link
		# and also a string to represent this part
		url = ''
		url_string = ''
		welcome = 'Welcome back'

		# pulling back the current user from the request
		user = users.get_current_user()

		if not user:
			return self.redirect("/")

		if self.request.get("cancel"):
			return self.redirect("/")

		name = self.request.get('name')

		mygpu_key = ndb.Key('MyGpu',name)
		mygpu = mygpu_key.get()
		mygpu.geometryShader = self.request.get('geometryShader') == "on"
		mygpu.tesselationShader = self.request.get('tesselationShader') == "on"
		mygpu.shaderInt16 = self.request.get('shaderInt16') == "on"
		mygpu.sparseBinding = self.request.get('sparseBinding') == "on"
		mygpu.textureCompressionETC2 = self.request.get('textureCompressionETC2') == "on"
		mygpu.vertexPipelineStoresAndAtomics = self.request.get('vertexPipelineStoresAndAtomics') == "on"

		mygpu.put()

		self.redirect("/")
