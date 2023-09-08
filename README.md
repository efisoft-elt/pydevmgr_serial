An pydevmgr_core extension for serial communication 



Sources are [here](https://github.com/efisoft-elt/pydevmgr_serial) 

Doc to comme


# Install

```bash
> pip install pydevmgr_serial 
```

# Basic Usage

Bellow is an exemple of implementation of a node that check a value from a Tesla Sensor. 
An extra configuration argument is added and the fget method is implemented. 

```python 
from pydevmgr_serial import BaseSerialNode
import time

    
class TesaNode(BaseSerialNode):
    class Config:
        delay: float = 0.1
        
    def fget(self):
        self.serial.write(b'?\r')
        time.sleep(self.config.delay)
        sval = self.serial.read(20)
        val = float(sval)
        return val
```

you can simply use the node with a Serial object :

```python 
from serial import Serial 

# build a standalone node 
com = Serial(port='COM1', baudrate=9600)
tesa = TesaNode(com=com)

print( "Position is ", tesa.get() )
com.close()

```

One can include the node in a serial device which will hold the communcation

Note: One creating a SerialDevice the port is not directly opened one needs to use
the ``connect`` method or within a with statement. 


```python 
from pydevmgr_serial import SerialDevice
from pydevmgr_core import nodealias



class Tesa(SerialDevice):    
    raw_pos = TesaNode.Config()
    
    @nodealias('raw_pos')
    def position(self, raw_pos):
        return 10 + 1.3 * raw_pos    
```

```python 
tesa = Tesa('tesa',  port ='COM1', baudrate=9600)

with tesa:
    tesa.position.get()
```



