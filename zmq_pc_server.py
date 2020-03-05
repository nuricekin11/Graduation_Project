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
def IdentProcess(ident):
#        ident=ident.decode()
        com_type_number=ident.decode()[:4]
        ident=ident.decode()[4:]
        if com_type_number == CommID.TV_TYPE_COMM:
            return RequestType.TV,ident
        if com_type_number == CommID.PC_TYPE_COMM:
            return RequestType.PC,ident    
def worker_thread(msg):

        
        print(type(msg))
        tprint('Worker received %s from ' % (msg))
        
        DeviceType,ID=IdentProcess(msg)
        if DeviceType == RequestType.PC:
#               ident, message =worker.recv_multipart()
#               print(message)
               
                
               
              
               
               worker.send_multipart([msg,Messages.PC_Definiton.encode()])
               print("message sent")
               Identity,target=worker.recv_multipart()
               print(target)
               tprint('Worker received %s ' % (target))

               worker.send_multipart([msg,Messages.Ready_File.encode()])
               Identity, file=worker.recv_multipart()
               
               tprint('Worker received %d byte ' % (len(file)))
               worker.send_multipart([msg,Messages.OK.encode()])
               backend = context.socket(zmq.DEALER)
               address = 'ipc://' + target.decode()
               print(address)
               backend.connect(address)
               print("Connected")
               backend.send(file)
               print("sended")
               file_return = backend.recv_multipart()
               print(file_return)
               worker.send_multipart([msg,file_return[0]])
               
               backend.close()

               
        if DeviceType == RequestType.TV:
                print(msg)
                

                worker.send_multipart([msg,Messages.PC_Definiton.encode()])
                ident , okmsg= worker.recv_multipart()
                print(okmsg)

                
                      
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
        print(ident)
        print(msg)
        tprint('Worker received %s from' % ident)
        
        """main function"""
        if msg:
            server = threading.Thread(target = worker_thread,args=(ident,))
            server.start()
            server.join()
            
            
#            continue
if __name__ == "__main__":
    main()    
