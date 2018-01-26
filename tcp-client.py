#!/bin/python

import socket

# Set target info
host = "www.linuxacademy.com"
port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host,port))
client.send("GET / HTTP/1.1\r\nHost: linuxacademy.com\r\n\r\n")

reply = client.recv(4096)

print reply
