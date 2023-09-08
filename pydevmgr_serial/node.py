from typing import Optional
from pydevmgr_core import BaseNode
from .engine import SerialEngine


class BaseSerialNode(BaseNode):
    Engine = SerialEngine
    
    @property
    def serial(self):
        return self.engine.serial

    
    @property
    def sid(self):
        # the port is the sid  
        return self.serial.port
     
    def fget(self):
        raise NotImplementedError('fget')
        
    def fset(self, value):
        raise NotImplementedError('fset')
        
