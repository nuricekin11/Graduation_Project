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
    try:
        file=open(directory,"rb")
        data=file.read()
    except:
        return 0
    return data
def ErrorController():
    if PC_Def_Error == 1:
        return -1
    elif Ready_File_Error == 1:
        return -1
    elif OK_Error == 1:
        return 1
    elif File_Return_Error == 1:
        return -1
    else:
        return 0

PC_Def_Error = 0
Ready_File_Error = 0
OK_Error = 0
File_Return_Error = 0
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
socket.RCVTIMEO = 3000
socket.SNDTIMEO = 3000
#socket.connect("tcp://3.125.40.81:5570")
socket.connect("tcp://localhost:5570")
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)
#target = [b'00:11:e1:63:c9:e2\n']
#file = "/home/nuric/Desktop/Bitirme/HelloWorld"

def sendFile(target,file):
    global PC_Def_Error
    global Ready_File_Error
    global OK_Error
    global File_Return_Error
    reqs = 0
    reqs = reqs + 1
    print('Req #%d sent..' % (reqs))
    socket.send_multipart([b'Hello'])
    
    try:
        msg = socket.recv_multipart()
        print(msg)
    except:
        PC_Def_Error=1
        print("No answer from server")
        
    if ErrorController():
        print("PC_Def_Error")
        return 0
    socket.send_multipart([target])
    
    try:
        msg = socket.recv_multipart()
        print(msg)
    except:
        Ready_File_Error = 1
        print("Server is not ready for file...")
    if ErrorController():
        return 0
    data = FileOpener(file)
    if not data:
        print("Directory not found. Please enter valid directory")
        return 0
    
    socket.send_multipart([data])
#    sockets = dict(poll.poll())
#    if socket in sockets:
    try:
        msg = socket.recv_multipart()
        print(msg)
    except:
        OK_Error = 1
        print("No answer from server...")
    if ErrorController():
        return 0    
        
    try:
        file_return = socket.recv_multipart()
        print(file_return)    
    except:
       File_Return_Error = 1
       print("No return from TV")
    if ErrorController():
        return 0     
    else:
       return 1
       
def main():
    while 1:
        target = input("Enter your target TV: ")
        target = target.encode()
        file = input("Enter your file: ")
        sendFile(target,file)
if __name__ == "__main__":
    main()