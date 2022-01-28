from pydantic import BaseModel, validator
from typing import Optional, Union 
from .serial_com import SerialCom, parse_com
from pydevmgr_core import BaseRpc, reconfig



class BaseSerialRpcConfig(BaseRpc.Config):   
    prefix: str = ""
    # include the possibility to include an optional com configuration for standalone com
    com: Optional[SerialCom.Config] = None
    

class BaseSerialRpc(BaseRpc):
    Config = BaseSerialRpcConfig
    Com = SerialCom
    def __init__(self, key, config=None, com=None, **kwargs): 
        # parse the config and com object 
        super().__init__(key, config=config, **kwargs) 
        self._com = parse_com(com, self._config.com)    
    
    @property
    def sid(self):
        self._com.sid
        
    def connect(self):
        self._com.connect()
    
    def disconnect(self):
        self._com.disconnect()
    
    def fcall(self, *args, **kwargs):
        raise NotImplementedError('fcall')
        
        
