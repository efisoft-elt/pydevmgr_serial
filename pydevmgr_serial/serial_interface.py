from typing import Optional 
from .serial_com import parse_com, SerialCom
from pydevmgr_core import BaseInterface



class BaseSerialInterfaceConfig(BaseInterface.Config):   
    prefix: str = ""
    # include the possibility to include an optional com configuration for standalone com
    com: Optional[SerialCom.Config] = None

    
class BaseSerialInterface(BaseInterface):
    Config = BaseSerialInterfaceConfig
    Com = SerialCom
    def __init__(self, 
           key: str, 
           config: Optional[BaseSerialInterfaceConfig] = None, 
           com: Optional[SerialCom] = None, 
           **kwargs
        ) -> None:
        # parse the config and com object                    
        super().__init__(key, config=config, **kwargs) 
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
    
    @classmethod
    def new_args(cls, parent, config):
        d = super().new_args(parent, config)
        d.update(com=parent.com)
        return d


