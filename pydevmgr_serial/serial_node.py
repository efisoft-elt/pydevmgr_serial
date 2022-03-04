from typing import Optional
from .serial_com import parse_com, SerialCom 
from pydevmgr_core import BaseNode



class BaseSerialNodeConfig(BaseNode.Config):   
    prefix: str = ""
    # include the possibility to include an optional com configuration for standalone com
    com: Optional[SerialCom.Config] = None
    

class BaseSerialNode(BaseNode):
    Config = BaseSerialNodeConfig
    Com = SerialCom
    def __init__(self, key, config=None, com=None, **kwargs): 
        # parse the config and com object 
            
        super().__init__(key, config=config, com=com, **kwargs)
        self._com = parse_com(com, self._config.com)


    @classmethod
    def new_args(cls, parent, config):
        d = super().new_args(parent, config)
        d.update(com=parent.com)
        return d

    @property
    def com(self):
        return self._com 
    
    @property
    def sid(self):
        self._com.sid
    
    def connect(self):
        self._com.connect()
    
    def disconnect(self):
        self._com.disconnect()
    
    def fget(self):
        raise NotImplementedError('fget')
        
    def fset(self, value):
        raise NotImplementedError('fset')
        
