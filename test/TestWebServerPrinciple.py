"""
------------------------------------------------------------
   File Name: TestWebServerPrinciple.py
   Description: WebServer Principle test
   Author: JockMing
   Date: 2020/03/21
------------------------------------------------------------
   Change Activity:
                   2020/03/21: WebServer Principle test
------------------------------------------------------------
"""
__author__ = 'JockMing'
import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)
    # In python 3, bytes strings and unicode strings are two different types
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    # The http_response in the program is a unicode string,
    # so a TypeError occurs because the socket uses a byte stream buffer.
    client_connection.sendall(http_response)
    client_connection.close()
