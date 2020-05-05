#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:01:25 2020

@author: nuric
"""

import zmq
import sys
import threading
from enum import Enum
import time
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import os




class CommID():
    TV_TYPE_COMM='0000'
    PC_TYPE_COMM='1111'
    
class RequestType(Enum):
        TV=1
        PC=2
        
class Messages():
      TV_Definition = 'You are TV'
      PC_Definiton = 'You are PC'
      OK="OK"
      Ready_File="Ready For File"

def ErrorController():
    if Target_Error == 1:
        return -1
    elif File_PC_Error == 1:
        return -1
    elif Backend_Connect_Error == 1:
        return -1
    elif File_Return_Error == 1:
        return -1
    else:
        return 0      
Target_Error = 0
File_PC_Error = 0
Backend_Connect_Error = 0
File_Return_Error = 0    
    
def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
        
        
    
def workerThread(msg):
    worker_func(msg)
    worker.RCVTIMEO = -1
    worker.SNDTIMEO = -1
    return     
    
#class ServerTask(threading.Thread):
#    """ServerTask"""
#    def __init__(self):
#        threading.Thread.__init__ (self)
def IdentProcessPC(ident):
#        ident=ident.decode()
        com_type_number=ident.decode()[:4]
        ident=ident.decode()[4:]
        if com_type_number == CommID.PC_TYPE_COMM:
            return RequestType.PC,ident 
        else:
            return 0,0
def worker_func(msg):
        global Target_Error
        global File_PC_Error
        global Backend_Connect_Error
        global File_Return_Error       
        worker.send_multipart([msg,Messages.PC_Definiton.encode()])
        try:
            Identity,target=worker.recv_multipart()
            tprint("Our target TV's mac address is: " + target.decode())
        except:
            Target_Error = 1
            tprint("Client does not send target TV")
        if ErrorController():
            return 0
        worker.send_multipart([msg,Messages.Ready_File.encode()])
        tprint("Ready File message sent")
        try:
            Identity, file=worker.recv_multipart()
            tprint("Server recevied program")
            tprint('Server received %d byte ' % (len(file)))
        except:
            File_PC_Error = 1
            tprint("Server did not receive file")
        if ErrorController():
            return 0   
        worker.send_multipart([msg,Messages.OK.encode()])
        backend = context.socket(zmq.DEALER)
        backend.RCVTIMEO = 3000
        backend.SNDTIMEO = 3000
        address = 'ipc://' + target.decode()
        tprint("Connecting TV...")
        try:
            backend.connect(address)
            tprint("Connected")
        except:
            Backend_Connect_Error = 1
            tprint("Server can not connect TVServer...")
        if ErrorController():
            return 0      
            
            
        backend.send(file)
        print("sended")
        try:
            file_return = backend.recv_multipart()
            print(file_return)
        except:
            File_Return_Error = 1
            tprint("No return from program")
        if ErrorController():
            return 0     
            
        worker.send_multipart([msg,file_return[0]])
      
        backend.close()
        
  
        

base_dir = os.path.dirname(__file__)
keys_dir = os.path.join(base_dir, 'certificates')
public_keys_dir = os.path.join(base_dir, 'public_keys')
secret_keys_dir = os.path.join(base_dir, 'private_keys')                
                    
context = zmq.Context().instance()
auth = ThreadAuthenticator(context)
auth.start()
auth.configure_curve(domain='*', location=public_keys_dir)
worker = context.socket(zmq.ROUTER)
worker.setsockopt(zmq.ROUTER_MANDATORY,1)
server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
worker.curve_secretkey = server_secret
worker.curve_publickey = server_public
worker.curve_server = True 
worker.bind('tcp://*:5570')  
       

def main():
    


    i = 0
    while 1:

        i+=1
        print(i)
        ident, msg = worker.recv_multipart()
        tprint('Worker received %s from %s' % (ident.decode(),msg.decode()))
        
        """main function"""
        if msg:
            worker.RCVTIMEO = 3000
            worker.SNDTIMEO = 3000
            if IdentProcessPC(ident):
                tprint("PC connected... ")
                server = threading.Thread(target = workerThread,args=(ident,))
                server.start()
                server.join()
            else:
                tprint("Other devices connected connected... ")
                continue
            
            
#            continue
if __name__ == "__main__":
    main()    
