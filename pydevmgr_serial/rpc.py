from typing import Optional
from pydevmgr_core import BaseRpc
from .engine import SerialEngine


class BaseSerialRpc(BaseRpc):
    Engine = SerialEngine

    @property
    def sid(self):
        self.serial.port
    
    @property
    def serial(self):
        return self.engine.serial
       
    def fcall(self, *args, **kwargs):
        raise NotImplementedError('fcall')
        
        
