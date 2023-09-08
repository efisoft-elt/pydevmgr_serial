from typing import Optional 
from pydevmgr_core import BaseInterface
from .engine import SerialEngine
import serial as sr

    
class SerialInterface(BaseInterface):
    Engine = SerialEngine
    
    @property
    def serial(self):
        return self.engine.serial

