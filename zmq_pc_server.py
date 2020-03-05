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
    
    
def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
    
    
    
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
def worker_thread(msg):
       

        worker.send_multipart([msg,Messages.PC_Definiton.encode()])
        Identity,target=worker.recv_multipart()
        tprint("Our target TV's mac address is: " + target.decode())
        worker.send_multipart([msg,Messages.Ready_File.encode()])
        tprint("Ready File message sent")
        Identity, file=worker.recv_multipart()
        tprint("Server recevied program")
        tprint('Server received %d byte ' % (len(file)))
        worker.send_multipart([msg,Messages.OK.encode()])
        backend = context.socket(zmq.DEALER)
        address = 'ipc://' + target.decode()
        tprint("Connecting TV")
        backend.connect(address)
        print("Connected")
        backend.send(file)
        print("sended")
        file_return = backend.recv_multipart()
        print(file_return)
        worker.send_multipart([msg,file_return[0]])
               
        backend.close()
        
  
        


            


                
                    
context = zmq.Context()
worker = context.socket(zmq.ROUTER)
worker.setsockopt(zmq.ROUTER_MANDATORY,1)
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
            if IdentProcessPC(ident):
                print("PC connected... ")
                server = threading.Thread(target = worker_thread,args=(ident,))
                server.start()
                server.join()
            else:
                print("Other devices connected connected... ")
                continue
            
            
#            continue
if __name__ == "__main__":
    main()    
