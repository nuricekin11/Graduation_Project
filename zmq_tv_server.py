#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:46:07 2020

@author: nuric
"""

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
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import time
import os 



class CommID():
    TV_TYPE_COMM='0000'
    PC_TYPE_COMM='1111'
    
class RequestType(Enum):
        TV=1
        PC=2
        
class Messages():
      TV_Definition = 'You are TV'
      PC_Definition = 'You are PC'
      OK="OK"
      Ready_File="Ready File"
    
    
def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
    
def ErrorController():
    if Ready_File_Error == 1:
        tprint("Server did not receive Ready File message")
        return -1
    elif File_TV_Error == 1:
        tprint("Server did not receive program")
        return -1
    elif Backend_Bind_Error == 1:
        tprint("Can not bind backend socket ")
        return -1
    elif File_Return_Error == 1:
        tprint("Server did not receive program output")
        return -1
    elif Chunk_Number_Error == 1:
        tprint("Server cant receive chunk number")
        return -1    
    else:
        return 0      
Ready_File_Error = 0
File_TV_Error = 0
Backend_Bind_Error = 0
File_Return_Error = 0
Chunk_Number_Error = 0        
    
#class ServerTask(threading.Thread):
#    """ServerTask"""
#    def __init__(self):
#        threading.Thread.__init__ (self)
def IdentProcessTV(ident):
#        ident=ident.decode()
        
        com_type_number=ident.decode()[:4]
        ident=ident.decode()[4:]
        
        if com_type_number == CommID.TV_TYPE_COMM:
            return RequestType.TV
        else:
            return 0
def workerThread(Communication_ID):
    worker_func(Communication_ID)
    worker.RCVTIMEO = -1
    worker.SNDTIMEO = -1        
def worker_func(Communication_ID):
    global File_TV_Error
    global Ready_File_Error
    global Backend_Bind_Error
    global File_Return_Error 
    global Chunk_Number_Error              
    ID = Communication_ID.decode()[4:]
    worker.send_multipart([Communication_ID, Messages.TV_Definition.encode()])
    try:
        Ident,msg= worker.recv_multipart()
        tprint("Ready File Received")
    except:
        Ready_File_Error = 1
    if ErrorController():
        return 0 
    backend = context.socket(zmq.ROUTER)
    backend.RCVTIMEO = -1
    backend.SNDTIMEO = -1 
    Backend_Socket_Name = ID[:-1]
    tprint("IPC socket name is: " + Backend_Socket_Name)
    address = 'ipc://' + Backend_Socket_Name
    try:
        backend.bind(address)
        tprint("Socket created")
    except:
        Backend_Bind_Error = 1
    if ErrorController():
        return 0
    try:
        Identity, chunk_number_byte = backend.recv_multipart()
        print(chunk_number_byte)
        chunk_number = int(chunk_number_byte.decode())
        worker.send_multipart([Communication_ID,chunk_number_byte])
    except:
        Chunk_Number_Error = 1
    if ErrorController():
        return 0
    backend.send_multipart([Identity,Messages.OK.encode()])
    
    for i in range(chunk_number):
        try:    
            Identity_Backend,file = backend.recv_multipart()
            tprint("%d byte received" %(len(file)))
            tprint("Chunk number %d" %(i))
            worker.send_multipart([Communication_ID,file])
            tprint("Program sent to TV")
        except:
            File_TV_Error = 1
        if ErrorController():
            return 0      
        

#    try:
    ident, file_return = worker.recv_multipart()
    tprint('Program output at TV:')
    print(file_return)
##    except:
#        File_Return_Error = 1
    if ErrorController():
        return 0     
    backend.send_multipart([Identity,file_return])
    print('Output sent to client PC')
    return 1
                    

base_dir = os.path.dirname(__file__)
keys_dir = os.path.join(base_dir, 'certificates')
public_keys_dir = os.path.join(base_dir, 'public_keys')
secret_keys_dir = os.path.join(base_dir, 'private_keys')                
                
context = zmq.Context().instance()
auth = ThreadAuthenticator(context)
auth.start()
auth.configure_curve(domain='*', location=public_keys_dir)
worker = context.socket(zmq.ROUTER)
server_secret_file = os.path.join(secret_keys_dir, "server.key_secret")
server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
worker.curve_secretkey = server_secret
worker.curve_publickey = server_public
worker.curve_server = True 
#worker.setsockopt(zmq.ROUTER_MANDATORY,1)
worker.bind('tcp://*:5571')  
       

def main():
    i = 0
    while 1:
        i+=1
        print(i)
        ident, msg = worker.recv_multipart()
        tprint('Worker received %s from %s' %(msg.decode(), ident.decode()))
        
        """main function"""
        if ident:
            worker.RCVTIMEO = 15000
            worker.SNDTIMEO = 15000
            if IdentProcessTV(ident):
                print("TV connected...")
                server = threading.Thread(target = workerThread,args=(ident,))
                server.start()
                server.join()
            else:
                ("Other devices connected...")
                continue
            
            
#            continue
if __name__ == "__main__":
    main()    
