#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# session
# http://bottlepy.org/docs/dev/recipes.html#keeping-track-of-sessions
# http://beaker.readthedocs.org
# http://beaker.readthedocs.org/en/latest/sessions.html
# http://beaker.readthedocs.org/en/latest/configuration.html
#
# debug
# http://bottlepy.org/docs/dev/recipes.html#debugging-with-style-debugging-middleware
# http://werkzeug.pocoo.org/docs/debug/#werkzeug.debug.DebuggedApplication

from pprint import pformat
import bottle
from bottle import request, response, abort, redirect
from bottle import run
from beaker.middleware import SessionMiddleware
from bottle_session import SessionPlugin

app = bottle.Bottle()
plugin = SessionPlugin(always=True)
app.install(plugin)

debug = True
reloader = True

# 如果不设置 type 和 data_dir 会使用 memory (无法多进程共享，仅用于测试，
#	比如，在调试的时候，每次修改后 reload 都会失去 session 信息)
# 如果不设置 type 而设置了 data_dir 会使用 file
# type 为 cookie 时，encrypt_key 用于加密，validate_key 用于签名
# auto 表示自动保存，默认不会自动保存需要调用 session.save()
# timeout 是 session 的失效时间，过期相当于调用了 session.invalidate()
# cookie_expires 是 cookie 的有效时间，过期浏览器就不会带上这个 cookie
#	True 表示会话类 Cookie (临时 Cookie)，关闭浏览器即失效
#	False 表示永不失效，默认值就是这个
#	datetime 明确的失效时间
#	int, timedelta 多久后失效，int 表示秒
session_opt = {
		'session.type': 'cookie',
		'session.auto': True,
		'session.cookie_expires': True,
		'session.timeout': 300,
		'session.encrypt_key': 'encrypt',
		'session.validate_key': 'validate',
		}

@app.route('/')
def hello():
	return 'Hello world'

@app.route('/env')
def env():
	response.content_type = 'text/plain'
	return pformat(request.environ)

@app.route('/count')
def count(session):
	session['count'] = session.get('count', 0) + 1
	return str(session['count'])

@app.route('/delete')
def delete(session):
	session.delete()

@app.route('/invalidate')
def invalidate(session):
	session.delete()
	session.invalidate()

@app.route('/info')
def info(session):
	response.content_type = 'text/plain'
	yield pformat(session)
	yield '\n\n'
	yield 'session.id = %s' % session.id
	# type 为 cookie 的 session 没有 last_accessed 属性
	if hasattr(session, 'last_accessed'):
		yield '\n'
		yield 'session.last_accessed = %s' % session.last_accessed 

@app.route('/error')
def error(session):
	raise Exception('Somthing is Wrong')

if __name__ == '__main__':
	if debug:
		try:
			from werkzeug.debug import DebuggedApplication
			app.catchall = False
			app = DebuggedApplication(app, evalex=True)
		except ImportError:
			pass
	app = SessionMiddleware(app, session_opt)
	run(app, host='localhost', port=8080, debug=debug, reloader=reloader)
