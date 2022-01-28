from pydantic import BaseModel, validator
from typing import Optional, Union 
from .serial_com import parse_com, SerialCom
from pydevmgr_core import BaseDevice, reconfig



class BaseSerialDeviceConfig(BaseDevice.Config):   
    prefix: str = ""
    # include the possibility to include an optional com configuration for standalone com
    com: SerialCom.Config = SerialCom.Config()
    
    
class BaseSerialDevice(BaseDevice):
    Config = BaseSerialDeviceConfig
    Com = SerialCom
    def __init__(self, 
           key: str, 
           config: Optional[BaseSerialDeviceConfig] = None, 
           com: Optional[SerialCom] = None, 
           **kwargs
        ) -> None:
        # parse config and com 
                 
        super().__init__(key, config=config,  **kwargs) 
        
        self._com = parse_com(com, self._config.com)
    
    
       
    
    @property
    def com(self):
        return self._com 
    
    def connect(self):
        """connect the serial com """
        self._com.connect()
    
    def disconnect(self):
        """disconnect serial com """
        self._com.disconnect()
    
    
