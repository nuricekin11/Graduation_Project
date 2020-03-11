#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:43:05 2020

@author: nuric
"""

import zmq
import time
import os 
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

def FileOpener(directory):
    file=open(directory,"rb")
    data=file.read()
    return data
base_dir = os.path.dirname(__file__)
keys_dir = os.path.join(base_dir, 'certificates')
public_keys_dir = os.path.join(base_dir, 'public_keys')
secret_keys_dir = os.path.join(base_dir, 'private_keys')    
#  Socket to talk to server
context = zmq.Context().instance()
socket = context.socket(zmq.DEALER)
client_secret_file = os.path.join(secret_keys_dir, "client.key_secret")
client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
socket.curve_secretkey = client_secret
socket.curve_publickey = client_public
server_public_file = os.path.join(public_keys_dir, "server.key")
server_public, _ = zmq.auth.load_certificate(server_public_file)
print("Connecting to server…")
socket.curve_serverkey = server_public
identity='11111515'
socket.identity = identity.encode()
socket.connect("tcp://127.0.0.1:5570")
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