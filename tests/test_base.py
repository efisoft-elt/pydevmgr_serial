import pytest 
from pydevmgr_serial import SerialDevice 




def test_engine_is_parsed_to_node():
    
    class D(SerialDevice):
        class I(SerialDevice.Interface):
            n = SerialDevice.Node.Config()
        i = I.Config()
        
    d = D()
    assert d.i.n.engine is d.engine


def test_engine_arguments():
    class D(SerialDevice):
        class I(SerialDevice.Interface):
            n = SerialDevice.Node.Config()
        i = I.Config()
        
    d = D(baudrate=5000, parity=D.PARITY.EVEN)
    assert d.engine.serial.baudrate == 5000
    assert d.engine.serial.parity == D.PARITY.EVEN

