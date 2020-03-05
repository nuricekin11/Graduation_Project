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
print("Connecting to server…")
socket = context.socket(zmq.DEALER)
identity='11111515'
socket.identity = identity.encode()
socket.connect("tcp://localhost:5570")
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
#target = [b'00:11:e1:63:c9:e2\n']
#file = "/home/nuric/Desktop/Bitirme/HelloWorld"
def sendFile(target,file):
    reqs = 0
    reqs = reqs + 1
    print('Req #%d sent..' % (reqs))
    socket.send_multipart([b'Hello'])
    
    msg = socket.recv_multipart()
    print(msg)
    
    
    socket.send_multipart([target])
    
    msg = socket.recv_multipart()
    print(msg)
    data = FileOpener(file)
    
    socket.send_multipart([data])
    sockets = dict(poll.poll())
    if socket in sockets:
        msg = socket.recv_multipart()
        print(msg) 
    file_return = socket.recv_multipart()
    print(file_return)    
   
def main():
    while 1:
        target = input("Enter your target TV: ")
        target = target.encode()
        file = input("Enter your file: ")
        sendFile(target,file)
if __name__ == "__main__":
    main()