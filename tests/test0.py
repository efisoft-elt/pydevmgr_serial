from pydevmgr_serial import BaseSerialNode, SerialDevice
from pydevmgr_core import NodeAlias
import pty
import os
import time
from threading import Thread 
import random 

class TesaNodeConfig(BaseSerialNode.Config):
    type : str = 'Tesa'
    delay: float = 0.02 
    
class TesaNode(BaseSerialNode):
    Config = TesaNodeConfig
    def fget(self): 

        print("FGETIING .... ")
        self.com.write(b'?\r')
        print("write done")
        self.com.flush()
        time.sleep(self.config.delay)
        
        sval = self.com.read(20)
        if not sval:
            return -9.99
        return float(sval)


class Tesa(SerialDevice, position=TesaNode.Config()):
    pass
    



class SerialSimu(Thread):
    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.running = False
        super().__init__()
    
    @property
    def port(self):
        return os.ttyname(self.slave)
    
    def quit(self):
        with os.fdopen(self.slave, "wb") as fd:
            fd.write(b'q\r')
            fd.flush()
        self.running = False
       
    def run(self):
        #with os.fdopen(self.master, "wb") as fw:
        print("HAAAAAAAAAA")
        
        self.running = True
        with os.fdopen(self.master, "w+b") as fd:
            print("FD", self.running)
            while self.running:            
                print("Reading ......")
                a = fd.read(2)      
                print("Reading OK")
                if a == b'q\r':
                        return                    
                if a:                           
                        #with os.fdopen(self.master, "wb") as fw:    
                        v = 3 + random.random() - 0.5            
                        fd.write( f'{v}'.encode())
                        fd.flush()
                time.sleep(0.01)
                print(".", end="")

if __name__ == "__main__":        
    t  = SerialSimu()
    print("Simu running on ", t.port)    
    tesa = Tesa('tesa', config={'port':t.port, 'timeout':0.1, 'write_timeout':1.0})
    tesa.connect()
    
    t.start()
    tesa.position.get()
    t.quit()
    tesa.disconnect()
        
    
