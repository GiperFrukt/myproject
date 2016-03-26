import socket
import os.path 

HOST, PORT = '127.0.0.1', 8000
BUFFER_SIZE = 1000;
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
listen_socket.bind(server_address)
listen_socket.listen(5)
print ('Serving HTTP on port %s ...' % PORT)


while True:
        conn, addr = listen_socket.accept()
        print('...connected from: ', addr) 
        request = conn.recv(BUFFER_SIZE)
        if len(request) != 0:
                print('...request: ', request) 
                res = request.split('\n')[0].split(' ')[1]
                path = ""
                path = '.' + res 
                if not os.path.isfile(path):
                        path ='./index.html' 
                print('...path: ', path) 
                file = open(path, 'rb')
                response = """HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n""" + file.read()
                file.close()
                conn.send(response)
        conn.close()
                #listen_socket.close()
    
