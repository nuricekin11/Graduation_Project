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
import time




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
def IdentProcess(ident):
#        ident=ident.decode()
        print(type(ident))
        com_type_number=ident.decode()[:4]
        ident=ident.decode()[4:]
        print(com_type_number,ident)
        if com_type_number == CommID.TV_TYPE_COMM:
            return RequestType.TV,ident
        if com_type_number == CommID.PC_TYPE_COMM:
            return RequestType.PC,ident    
def worker_thread(Communication_ID):

        
        print(type(Communication_ID))
        tprint('Worker received %s from ' % (Communication_ID))
        
        DeviceType,ID=IdentProcess(Communication_ID)
        if DeviceType == RequestType.PC:
            
            
               worker.send_multipart([Communication_ID,Messages.PC_Definition.encode()])
               print("message sent")
               Identity,target=worker.recv_multipart()
               print(target)
               tprint('Worker received %s ' % (target))

               worker.send_multipart([Communication_ID,Messages.Ready_File.encode()])
               Identity, file=worker.recv_multipart()
               
               tprint('Worker received %d byte ' % (len(file)))
               worker.send_multipart([Communication_ID,Messages.OK.encode()])
               backend = context.socket(zmq.REQ)
               address = 'ipc://' + target
               backend.connect(address)
               backend.send_multipart([file])
               backend.close()

               
        if DeviceType == RequestType.TV:
                print("Communication_ID: ")
                print(Communication_ID)
#                Ident, recv_msg = worker.recv_multipart()
#                print("recv_msg: ")
#                print(recv_msg)
#                print("Ident: ")
#                print(Ident)
                time.sleep(0.5)
                worker.send_multipart([Communication_ID, Messages.TV_Definition.encode()])
                Ident,msg= worker.recv_multipart()
                print(Ident,msg)
                if msg.decode() == Messages.Ready_File:
                    backend = context.socket(zmq.ROUTER)
                    address = 'ipc://' + 'deneme'
                    print(address)
                    backend.bind(address)
                    print("socket opened")
                    file = backend.recv_multipart()
                    print("file recevied")
                    
                    
                    worker.send_multipart([Communication_ID,file[1]])
                    ident, file_return = worker.recv_multipart()
                    print('ident: ')
                    print(ident)
                    print('file_Return: ')
                    print(file_return)
                    backend.send_multipart([file[0],file_return])
                    

                
                
context = zmq.Context()
worker = context.socket(zmq.ROUTER)
#worker.setsockopt(zmq.ROUTER_MANDATORY,1)
worker.bind('tcp://*:5571')  
       

def main():
    i = 0
    while 1:
        i+=1
        print(i)
        ident, msg = worker.recv_multipart()
        print("Ident: ")
        print(ident)
        print(msg)
        tprint('Worker received %s from' % ident)
        
        """main function"""
        if ident:
            server = threading.Thread(target = worker_thread,args=(ident,))
            server.start()
            server.join()
            
            
#            continue
if __name__ == "__main__":
    main()    
