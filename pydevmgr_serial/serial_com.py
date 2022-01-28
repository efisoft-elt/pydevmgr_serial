""" lab interface for serial communication """
from pydantic import BaseModel, validator
from enum import Enum
import serial as sr
from typing import Optional, Union 
from pydevmgr_core import kjoin

# Copying serial constant into Enumerator, this will be used by the pydantic model 
class BITSIZE(int, Enum):
    FIVE  = sr.FIVEBITS
    SIX   = sr.SIXBITS
    SEVEN = sr.SEVENBITS
    EIGHT = sr.EIGHTBITS

class PARITY(str, Enum):
    NONE  = sr.PARITY_NONE
    EVEN  = sr.PARITY_EVEN
    ODD   = sr.PARITY_ODD 
    MARK  = sr.PARITY_MARK
    SPACE = sr.PARITY_SPACE

class STOPBITS(float, Enum):
    ONE = sr.STOPBITS_ONE
    ONE_POINT_FIVE = sr.STOPBITS_ONE_POINT_FIVE
    TWO = sr.STOPBITS_TWO



class SerialComConfig(BaseModel):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    prefix : str = "" # can be used to have a hiearchy in sub communication 
    #----------- from serial.Serial --------------------------------
    port : str = ""
    baudrate: int = 9600
    bytesize:  BITSIZE = BITSIZE.EIGHT
    parity: PARITY = PARITY.NONE
    stopbits: STOPBITS = STOPBITS.ONE
    timeout: Optional[float] = None
    xonxoff: bool = False 
    rtscts: bool = False
    write_timeout: Optional[float] = None 
    inter_byte_timeout: Optional[float] = None
    exclusive: Optional[bool] = None
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:
        use_enum_values = True



class _SerialSubCom:
    """ Wrapper around the :class:`serial.Serial` object 
    
    Providing basic method interface for pydevmgr. 
    """
    def __init__(self, prefix: str, serial: sr.Serial):
        self._prefix = prefix 
        self._serial = serial 
    
    def subcom(self, suffix: str) -> '_SerialSubCom':
        return _SerialSubCom(kjoin(self.prefix, suffix), self._serial)
    
    def connect(self):
        raise RuntimeError("Cannot connect a subcom, use the master com to connect")
    
    def disconnect(self):
        raise RuntimeError("Cannot disconnect a subcom, use the master com to disconnect")        
            
    @property
    def sid(self) -> str:
        """ The port name gives the sid not a big deal here """
        return self._serial.port
    
    @property
    def serial(self) -> sr.Serial:
        return self._serial
    
    @property
    def prefix(self) -> str:
        return self._prefix
    
        
class SerialCom:
    """ Com Wrapper for the serial.Serial object 
    
    The connection (opening of the serial port) is done after connect method is called
    
    Args:
       config (optional, :class:`SerialComConfig`, dict): serial com configuration 
       serial (optional): if a :class:`Serial` object is given it used as is and all other
                          config parameter are ignored. 
                          It is assumed that when a :class:`serial.Serial` object is given 
                          the connection is already opened. 
       **kwargs: If config is None any argument is used to build the Serial config
    """
    Config = SerialComConfig
    BITSIZE = BITSIZE
    PARITY = PARITY
    STOPBITS = STOPBITS
    
    def __init__(self, 
          config: SerialComConfig =None, 
          serial : sr.Serial =None,
          prefix : str = "", 
          **kwargs
         ) -> None:        
        self._is_slave = serial is not None
        
        if serial is None:
            if config is None:
                config = self.Config.parse_obj(kwargs)
            elif isinstance(config, dict):
                config = self.Config.parse_obj({**config, **kwargs})
                
            # open a serial com the port is excluded to avoid connection 
            # the connection is done by the connect method
            serial = sr.Serial(**config.dict(exclude={'port','prefix'}))
            serial.port = config.port
        
        self._prefix = prefix 
        self._config = config # config is not relevant after the the serial has been created
        self._serial = serial 
        
    @property
    def sid(self) -> str:
        """ The port name gives the sid not a big deal here """
        return self._serial.port
    
    @property
    def serial(self) -> sr.Serial:
        return self._serial
    
    @property
    def prefix(self) -> str:
        return self._prefix
    
    @property
    def config(self) -> Config:
        return self._config

    def connect(self) -> None:
        """ open serial communication """
        if self._is_slave:
            raise RuntimeError("Cannot connect connection must be established by the parent com")
        self._serial.open()
    
    def disconnect(self) -> None:
        """ disconnecting serial port """
        if self._is_slave:
            raise RuntimeError("Cannot disconnect connection must be closed by the parent com")
        self._serial.close()
        
    def subcom(self, suffix: str = "") -> _SerialSubCom:
        return _SerialSubCom(kjoin(self.prefix, suffix), self._serial)
        
          

def parse_com(com: Optional[Union[SerialCom, sr.Serial, str]], config: BaseModel) -> SerialCom:
    """ From a com object and a config return a valid :class:`SerialCom` 

    Args:
        com (None, :class:`SerialCom`, :class:`sr.Serial`, str): 
            If string this shall be the port name
        config (BaseModel, dict): Only used if com is None or a string. If com is a string, it overwrite 
            any .com defined in config. The SerialCom will receive a copy of this config
    """
    if com is None:
       com = SerialCom(config=config)            
    elif isinstance(com, (dict, BaseModel)):
        com = SerialCom(config=com)
    elif isinstance(com, sr.Serial):
        com = SerialCom(serial=com)
    elif isinstance(com, str):
        config = dict(config, port=com) 
        com = SerialCom(config=config)     
    return com

    
    
    
