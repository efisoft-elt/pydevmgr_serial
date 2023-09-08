from dataclasses import dataclass
from typing import Optional
try:
    from pydantic.v1.main import BaseModel
except ModuleNotFoundError:
    from pydantic.main import BaseModel
from pydevmgr_core import BaseEngine
import serial as sr
from enum import Enum

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


# port is left in purpose do not add it 
_serials_args= {'baudrate', 'bytesize', 'parity', 'stopbits', 'timeout', 
    'xonxoff', 'rtscts', 'write_teimout',
    'inter_byte_teimout', 'exclusive'}

def _new_serial(config: BaseModel) -> sr.Serial:
    return sr.Serial( **config.dict( include=_serials_args ) )
           
@dataclass
class SerialEngine(BaseEngine):
    serial: sr.Serial = None
    
    BITSIZE = BITSIZE
    PARITY = PARITY
    STOPBITS = STOPBITS

    class Config(BaseModel):
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
    
    @classmethod
    def new(cls, com=None, config = None):
        if isinstance(com, SerialEngine): return com 

        if config is None:
            config = cls.Config()
         
        engine = super().new(com, config)
        
        if com is None:
            serial = _new_serial(config)  
            serial.port = config.port
        elif isinstance(com, sr.Serial):
            serial = com 
        elif isinstance(com, dict):
            kwargs = {**config.dict(include=_serials_args), **com}
            port = kwargs.pop("port", "")
            serial = sr.Serial(**kwargs)
            serial.port = port 
            
        elif isinstance(com, str):
            serial = _new_serial(config)
            serial.port = com 
        elif isinstance(com, BaseEngine): 
            serial = _new_serial(config)
            serial.port = config.port 
         
        engine.serial = serial 
        return engine 




class SerialComHandler:
    
    def connect(self, engine: SerialEngine):
        engine.serial.port = engine.port 
        engine.serial.open()

    def disconnect(self, engine):
        engine.serial.close()
    
    def get_sid(self, engine):
        return engine.port 

    def write(self, engine, message):
        engine.serial.write( message)
    
    def read(self, engine, length):
        return engine.serial.read(length)
    
    def flush(self, engine):
        engine.serial.flush()
    
