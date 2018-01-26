#!/bin/python

import socket

# Set target info
host = "127.0.0.1"
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host,port))
client.send("ABCDEF\r\n")

reply = client.recv(4096)

print reply
