# -*- coding: utf-8 -*-

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


import os
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


answer = MyMiddleWare(app)
if __name__ == '__main__':
        from waitress import serve
        serve(answer, host='127.0.0.1', port=8000)
