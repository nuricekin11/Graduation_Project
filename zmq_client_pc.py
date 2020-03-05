#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:43:05 2020

@author: nuric
"""

import zmq
import time


context = zmq.Context()
def FileOpener(directory):
    file=open(directory,"rb")
    data=file.read()
    return data
    
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.DEALER)

identity='11111515'
socket.identity = identity.encode()
socket.connect("tcp://localhost:5570")
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
reqs = 0
reqs = reqs + 1
print('Req #%d sent..' % (reqs))
socket.send_multipart([b'Hello'])

msg = socket.recv_multipart()
print(msg)


socket.send_multipart([b'deneme'])

msg = socket.recv_multipart()
print(msg)
data = FileOpener("/home/nuric/Desktop/Bitirme/HelloWorld")

socket.send_multipart([data])
sockets = dict(poll.poll())
if socket in sockets:
    msg = socket.recv_multipart()
    print(msg) 
file_return = socket.recv_multipart()
print(file_return)    
   
#poll = zmq.Poller()
#poll.register(socket,zmq.POLLIN)
#socket.send_string(identity)
#msg = socket.recv()
#print(msg)
#
#print("deneme")    
##a=socket.recv_string()
##print(a)
#socket.send_multipart('OK'.encode('ascii'))
#print(socket.recv_string())
#socket.send_multipart(FileOpener("Mail"))
#print(socket.recv_string())



#  Do 10 requests, waiting each time for a response
