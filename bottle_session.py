# -*- coding: utf-8 -*-


# http://bottlepy.org/docs/dev/plugindev.html
'''
Usage Example::

	import bottle
	from bottle_session import SessionPlugin

	app = bottle.Bottle()
	plugin = SessionPlugin(always=True)
	app.install(plugin)

	@app.route('/count')
	def hello(session):
		session['count'] = session.get('count', 0) + 1
		return str(session['count'])

	session_opts = {
		'session.cookie_expires': True,
		'session.auto': True
	}
	app = SessionMiddleware(app, session_opts)
	bottle.run(app)
'''

import inspect
from bottle import request
from bottle import PluginError


class SessionPlugin(object):

	name = 'session'
	api  = 2

	def __init__(self, always=False, keyword='session'):
		'''
		@param always 
			True : each request will refresh the access_time of session
			False : refresh the access_time only when it needed
		'''
		self.always = always
		self.keyword = keyword

	def setup(self, app):
		''' Make sure that other installed plugins don't affect the same
			keyword argument.'''
		for other in app.plugins:
			if not isinstance(other, SessionPlugin): continue
			if other.keyword == self.keyword:
				raise PluginError("Found another session plugin with "\
						"conflicting settings (non-unique keyword).")

	def apply(self, callback, route):
		# Test if the original callback accepts a 'session' keyword.
		# Ignore it if it does not need a session.
		args = inspect.getargspec(route.callback)[0]
		has_keyword = self.keyword in args
		if not has_keyword and not self.always:
			return callback

		def wrapper(*args, **kwargs):
			session = request.environ['beaker.session']
			# update access_time
			session.id
			if has_keyword:
				kwargs[self.keyword] = session
			rv = callback(*args, **kwargs)
			return rv

		# Replace the route callback with the wrapped one.
		return wrapper

Plugin = SessionPlugin
