from typing import Optional
from .node import BaseSerialNode 
from .rpc import BaseSerialRpc 
from .interface import SerialInterface
from .engine import SerialEngine, BITSIZE, PARITY, STOPBITS 
import serial as sr

from pydevmgr_core import BaseDevice
 
class SerialDevice(BaseDevice):
    class Config(BaseDevice.Config, SerialEngine.Config):
        pass 
        
    Node = BaseSerialNode
    Rpc = BaseSerialRpc
    Interface = SerialInterface 
    Engine = SerialEngine


    BITSIZE = BITSIZE
    PARITY = PARITY
    STOPBITS = STOPBITS
    
    @property
    def serial(self):
        return self.engine.serial
    
    def connect(self):
        """connect the serial com """
        self.serial.open()
    
    def disconnect(self):
        """disconnect serial com """
        self.serial.close()
    
    
