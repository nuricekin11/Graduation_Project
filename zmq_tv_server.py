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
def worker_thread(Communication_ID):

               


                ID = Communication_ID.decode()[4:]
#                Ident, recv_msg = worker.recv_multipart()
#                print("recv_msg: ")
#                print(recv_msg)
#                print("Ident: ")
#                print(Ident)
                worker.send_multipart([Communication_ID, Messages.TV_Definition.encode()])
                Ident,msg= worker.recv_multipart()
                
                if msg.decode() == Messages.Ready_File:
                    print("Ready File Received")
                    backend = context.socket(zmq.ROUTER)
                    Backend_Socket_Name = ID[:-1]
                    print("IPC socket name is: " + Backend_Socket_Name)
                    address = 'ipc://' + Backend_Socket_Name
                    backend.bind(address)
                    print("Socket created")
                    file = backend.recv_multipart()
                    print("Program recevied")
                    worker.send_multipart([Communication_ID,file[1]])
                    print("Program sent to TV")
                    ident, file_return = worker.recv_multipart()
                    print('Program output at TV:')
                    
                    backend.send_multipart([file[0],file_return])
                    print('Output sent to client PC')
                    
                else:
                    print("Not Ready File Received")
                    

base_dir = os.path.dirname(__file__)
keys_dir = os.path.join(base_dir, 'certificates')
public_keys_dir = os.path.join(base_dir, 'public_keys')
secret_keys_dir = os.path.join(base_dir, 'private_keys')                
                
context = zmq.Context().instance()
auth = ThreadAuthenticator(context)
auth.start()
auth.allow("10.12.0.14")
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
            if IdentProcessTV(ident):
                print("TV connected...")
                server = threading.Thread(target = worker_thread,args=(ident,))
                server.start()
                server.join()
            else:
                ("Other devices connected...")
                continue
            
            
#            continue
if __name__ == "__main__":
    main()    
