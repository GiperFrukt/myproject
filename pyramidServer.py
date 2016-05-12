# -*- coding: utf-8 -*-
import os
import sys

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

MIDDLEWARE_TOP = "<div class='top'>Middleware TOP</div>"
MIDDLEWARE_BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"

class MyMiddleWare(object):
		def __init__(self, app):
			self.app = app

		def __call__(self, environ, start_response):
			response = self.app(environ, start_response)[0].decode()
			if response.find('<body>') == True:
				#разделяем документ на кусок до <Body> и после
				beforeBody,remainder = response.split('<body>')
				#оставшуюся часть делим на тело файла и концовку
				body,htmlend = remainder.split('</body>')
				#в тело документа вставляем мидлваровский код
				bodycontent = '<body>'+ MIDDLEWARE_TOP + bodycontent + MIDDLEWARE_BOTTOM+'</body>'
				return [beforeBody.encode() + body.encode() + htmlend.encode()]
			else:
				return [MIDDLEWARE_TOP + response.encode() + MIDDLEWARE_BOTTOM]


@wsgiapp
def app(environ, start_response):
        #Генерируем ответ на запрос
		res = environ['PATH_INFO']
		path = "."+res
		if not os.path.isfile(path):
			path ='./index.html' 
		print('...path: ', path)
		file = open(path,'rb')
		fileContent = file.read()
		file.close() 	
 		
		start_response('200 OK', [('Content-Type', 'text/html')])
		return [fileContent.encode()]



if __name__ == '__main__':
        config = Configurator()
    
        config.add_route('index', '/index.html')
        config.add_route('indexDefault', '/')
        config.add_route('aboutme', '/about/aboutme.html')

        config.add_view(app, route_name='index')
        config.add_view(app, route_name='indexDefault')
        config.add_view(app, route_name='aboutme')

        pyramid_app = config.make_wsgi_app()
        answer = MyMiddleWare(pyramid_app)

        server = make_server('0.0.0.0', 8000, answer)
        server.serve_forever()
