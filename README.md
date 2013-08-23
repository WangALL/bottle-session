bottle-session
==============

一个 [bottle](http://bottlepy.org) 的插件，
让你可以在 bottle 中使用 session 。

session 由 [Beaker](http://beaker.readthedocs.org) 提供。

使用方法：

	import bottle
	from bottle_session import SessionPlugin
	from beaker.middleware import SessionMiddleware
	
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

本插件只是略微简化了一些代码而已，比如：

不需要在使用 session 时，每次都写：

	@app.route('/hello')
	def hello():
		session = bottle.request.environ['beaker.session']
		...

只需要：

	@app.route('/hello')
	def hello(session):
		...

如果有一些请求不需要用到 session ，但是又希望刷新 session
的访问时间，避免 session 过期，只需要将 always 设置为 True ，
并且设置 session\_opts 的 session.auto 为 True：

	plugin = SessionPlugin(always=True)
