#!/usr/bin/python
# encoding=utf-8

from distutils.core import setup

version = '0.1'

setup(name='bottle-session',
	  version=version,
	  description='use session in bottle',
	  author='leiqin',
	  author_email='leiqin2010@gmail.com',
	  url='https://github.com/leiqin/bottle-session',
	  py_modules=['bottle_session'],
	  license='LGPL-3+',
	  requires=['bottle','beaker'],
	  )
