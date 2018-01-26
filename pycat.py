#!/bin/python

import sys
import socket
import getopt
import threading
import subprocess

listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def usage():
        print "PyCat Net Tool"
        print
        print "Usage: pycat.py -t target_host -p port"
        print "-l --listen              - listen on [host]:[port] for incoming connections"
        print "-e --execute=file_to_run - execute the given file upon receiving a connection"
        print "-c --command             - initialize a command shell"
        print "-u --upload=destination  - upon receiving connection upload a file and write to [destination]"
        print
        print
        print "Examples: "
        print "pycat.py -t 192.168.0.1 -p 5555 -l -c"
        print "pycat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
        print "pycat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
        print "echo 'ABCDEFGHI' | ./pycat.py -t 192.168.0.25 -p 135"
        sys.exit(0)

def main():
        global listen
        global port
        global execute
        global command
        global upload_destination
        global target

        if not len(sys.argv[1:]):
                usage()

        try:
                opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                ["help","listen","execute","target","port","command","upload"])
        except getopts.GetoptError as err:
                print str(err)
                usage()

        for o,a in opts:
                if o in ("-h","--help"):
                        usage()
                elif o in ("-l","--listen"):
                        listen = True
                elif o in ("-e", "--execute"):
                        execute = a
                elif o in ("-c", "--commandshell"):
                        command = True
                elif o in ("-u", "--upload"):
                        upload_destination = a
                elif o in ("-t", "--target"):
                        target = a
                elif o in ("-p", "--port"):
                        port = int(a)
                else:
                        assert False,"Unhandled Option"

        if not listen and len(target) and port > 0:

                buffer = sys.stdin.read()

                client_sender(buffer)

        if listen:
                server_loop()

def client_sender(buffer):
        
        client = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)

        try:
                client.connect(target,port)

                if len(buffer):
                        client.send(buffer)

                while True:
                        recv_len = 1
                        response = ""

                        while recv_len:
                                data     = client.recv(4096)
                                recv_len = len(data)
                                response+= data

                                if recv_len < 4096:
                                        break

                        print response,

                        buffer = raw_input("")
                        buffer += "\n"

                        client.send(buffer)

        except:
                print "[*] Exception! Exiting."
                client.close()

main()
