#!/usr/bin/python

from bottle import route, run, template, post, request

global tempdict

@post('/temperature', method="POST")
def index():
	global tempdict
	tempdict = dict(request.forms)
	print(tempdict['temp'])
#	temp(tempdictionary)

@route('/temp')
def temp():
	temp = tempdict['temp']
	curtime = tempdict['time']
	return curtime, " UTC\n", temp
run(host='0.0.0.0', port=8080)

