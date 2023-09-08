from pydevmgr_serial import BaseSerialNode, SerialDevice
from pydevmgr_core import NodeAlias
import pty
import os
import time
from threading import Thread 
import random 

    
class TesaNode(BaseSerialNode):
    class Config:
        delay: float = 0.02
    
    def fget(self): 

        print("FGETIING .... ")
        self.serial.write(b'?\r')
        print("write done")
        self.serial.flush()
        time.sleep(self.config.delay)
        
        sval = self.serial.read(20)
        if not sval:
            return -9.99
        return float(sval)


class Tesa(SerialDevice):
    position = TesaNode.Config()
    
class SerialSimu(Thread):
    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.running = False
        self.value = 1.0
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
                        fd.write( f'{self.value}'.encode())
                        fd.flush()
                time.sleep(0.01)
                print(".", end="")



# def test_node_get_with_simulator():
if __name__=="__main__":
    t  = SerialSimu()
    tesa = Tesa('tesa', config={'port':t.port, 'timeout':0.1, 'write_timeout':1.0})
    tesa.connect()
    t.start()
    assert tesa.position.get() == 1.0
    t.value = 99.99
    assert tesa.position.get() == 99.99
    t.quit()
    tesa.disconnect()
        
    
