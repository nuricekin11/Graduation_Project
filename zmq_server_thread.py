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
    
    
    
class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        
        worker = ServerWorker(context)
        worker.start()
        workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()
        
        
        
class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context
    def IdentProcess(self,ident):
        ident=ident.decode()
        com_type_number=ident[:4]
        print(type(com_type_number))
        ident=ident[4:]
        print(type(CommID.PC_TYPE_COMM))
        if com_type_number == CommID.TV_TYPE_COMM:
            return RequestType.TV,ident
        if com_type_number == CommID.PC_TYPE_COMM:
            return RequestType.PC,ident
#    def FileHandler(self,file_data):
         
         
        
        

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        tprint('Worker started')
        while True:
            ident, msg,a = worker.recv_multipart()
            tprint('Worker received %s from %s,%s' % (msg, ident, a))
            DeviceType,ID=self.IdentProcess(ident)
            if DeviceType == RequestType.PC:
                
               print(type(Messages.PC_Definiton))
               worker.send_string(Messages.PC_Definiton)
               a,ident,Identify_Answer=worker.recv_multipart()
               print(a,ident,Identify_Answer)
               tprint('Worker received %s ' % (Identify_Answer))
               worker.send_string(Messages.Ready_File)
               file=worker.recv_multipart()
               tprint('Worker received %d byte ' % (len(file)))
               worker.send_string(Messages.OK)
               
               
               
                
                
                
            
            

        worker.close()

#class PCWorker(threading.Thread):
#    """Handle PC Request"""
#    def __init__(self, context):
#        threading.Thread.__init__ (self)
#        self.context = context
#    def SerialController(serial_number):
#        if serial_number in serial_number_list:
#            return 1
#        else:
#            return 0
#        
#        
#    def run(self,ident,message):
#        
#    if SerialController(ident):
        
        
        
        
        
        
    
         
         
   
       

def main():
    """main function"""
    server = ServerTask()
    server.start()  
    server.join()
if __name__ == "__main__":
    main()    