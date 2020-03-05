#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:32:05 2020

@author: nuric
"""

import zmq
import time
import re, uuid 
import os
import subprocess

class Header:
    TV_HEADER = '0000'
    PC_HEADER = '1111'
    
class Messages:
      Hello = 'Hello'
      TV_Definition = 'You are TV'
      PC_Definition = 'You are PC'
      OK="OK"
      Ready_File="Ready For File"
      ERROR = 'Wrong Messages'

def getMAC(interface='eth0'):
  # Return the MAC address of the specified interface
    
    return (':'.join(re.findall('..', '%012x' % uuid.getnode())))    
context = zmq.Context()
print("Connecting to hello world server…")
socket = context.socket(zmq.DEALER)
IDENTITY = Header.TV_HEADER + getMAC()
socket.identity = IDENTITY.encode()


def main():
    socket.connect("tcp://localhost:5571")
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    reqs = 0
    reqs = reqs + 1
    print('Req #%d sent..' % (reqs))
    socket.send_multipart([Messages.Hello.encode()])
    msg = socket.recv_multipart()
    print(msg)
    if msg[0].decode() == Messages.TV_Definition:
        socket.send_multipart([Messages.Ready_File.encode()])
        file = socket.recv_multipart()
        print(file)
        target_file = open("targetfile", "wb")
        target_file.write(file[0])
        target_file.close()
        os.system("chmod +x targetfile")
        output = subprocess.check_output(['./targetfile'])
        print(output)
        socket.send_multipart([output])
        return 1
        
        
    else:
        socket.send_multipart([Messages.ERROR.encode()])
        return -1
    
if __name__ == "__main__":
    main()