# from periphery import I2C
from enum import IntEnum
import math
import time

class Pin(IntEnum):
    P0_0 = (1 << 0) 
    P0_1 = (1 << 1)
    P0_2 = (1 << 2)
    P0_3 = (1 << 3)
    P0_4 = (1 << 4)
    P0_5 = (1 << 5)
    P0_6 = (1 << 6)
    P0_7 = (1 << 7)

    P1_0 = (1 << 0) + (1 << 8)
    P1_1 = (1 << 1) + (1 << 8)
    P1_2 = (1 << 2) + (1 << 8)
    P1_3 = (1 << 3) + (1 << 8)
    P1_4 = (1 << 4) + (1 << 8)
    P1_5 = (1 << 5) + (1 << 8)
    P1_6 = (1 << 6) + (1 << 8)
    P1_7 = (1 << 7) + (1 << 8)

class Mode(IntEnum):
    OUTPUT = 0
    INPUT = 1

class Value(IntEnum):
    HIGH = 1  
    LOW = 0

class TCA9535():
    def __init__(self, i2c_bus='/dev/i2c-1', address=0x20):
        # I2C bus
        # self.i2c = I2C(i2c_bus)

        # i2c address
        self.address = address

        # Control registers address 
        self.INPUT_PORT_0_ADDR = 0x00 
        self.INPUT_PORT_1_ADDR = 0x01
        self.OUTPUT_PORT_0_ADDR = 0x02
        self.OUTPUT_PORT_1_ADDR = 0x03
        self.POLARITY_INV_PORT_0_ADDR = 0x04
        self.POLARITY_INV_PORT_1_ADDR = 0x05
        self.CONF_PORT_0_ADDR = 0x06
        self.CONF_PORT_1_ADDR = 0x07

        # Control register values
        self.INPUT_PORT_0 = 0x00 
        self.INPUT_PORT_1 = 0x02
        self.OUTPUT_PORT_0 = 0xFF
        self.OUTPUT_PORT_1 = 0xFF
        self.POLARITY_INV_PORT_0 = 0x00
        self.POLARITY_INV_PORT_1 = 0x00
        self.CONF_PORT_0 = 0xFF
        self.CONF_PORT_1 = 0xFF
    
    def pin_mode(self, pin, mode):
        print("Pin Mode")
        
        p = int(pin)
        m = int(mode)

        # PORT_1 (P1_0, ... P1_7)        
        if p > (1 << 7 + 1):
            print(">PORT_1")
            p = p % (1 << 8)
            # mode
            if m:
                # input mode
                self.CONF_PORT_1 = self.CONF_PORT_1 | p
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_1:{0:b}".format(self.CONF_PORT_1))
            else:
                # output mode
                self.CONF_PORT_1 = self.CONF_PORT_1 & ~p        
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_1:{0:b}".format(self.CONF_PORT_1))
        # PORT_0 (P0_0, ... P0_7)
        else:
            # mode
            print(">PORT_0")
            if m:
                # input mode
                self.CONF_PORT_0 = self.CONF_PORT_0 | p
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_0:{0:b}".format(self.CONF_PORT_0))

            else:
                # output mode
                self.CONF_PORT_0 = self.CONF_PORT_0 & ~p
                print(">>Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print(">>>CONF_PORT_0:{0:b}".format(self.CONF_PORT_0))        

    def digital_write(self, pin, value):
        print("digital_write")
        p = int(pin)
        v = int(value)
        # PORT_1 (P1_0, ... P1_7)        
        if p > (1 << 7 + 1 ):
            p = p % (1 << 8)
            print(">PORT_1")
            # value
            if v:
                # high value
                self.OUTPUT_PORT_1 = self.OUTPUT_PORT_1 | p
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_1:{0:b}".format(self.OUTPUT_PORT_1)) 
            else:
                # low value
                self.OUTPUT_PORT_1 = self.OUTPUT_PORT_1 & ~p        
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_1:{0:b}".format(self.OUTPUT_PORT_1))
        # PORT_0 (P0_0, ... P0_7)
        else:
            print(">PORT_0")
            # value
            if v:
                # high value
                self.OUTPUT_PORT_0 = self.OUTPUT_PORT_0 | p
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_0:{0:b}".format(self.OUTPUT_PORT_0)) 
            else:
                # low value
                self.OUTPUT_PORT_0 = self.OUTPUT_PORT_0 & ~p        
                print(">>Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print(">>>OUTPUT_PORT_0:{0:b}".format(self.OUTPUT_PORT_0))
 
        
    def digital_read(self, pin):
        print("digital_read")
        p = int(pin)
        
        # PORT_1 (P1_0, ... P1_7)        
        if p > (1 << 7 + 1 ):
            p = p % (1 << 8)
            # Read I2C PORT_1
            r = (self.INPUT_PORT_1 & p) >> int(math.log2(p))
            if r:
                return Value.HIGH
            else:
                return Value.LOW
        # PORT_0 (P0_0, ... P0_7)
        else:
            # Read I2C PORT_0
            r = (self.INPUT_PORT_0 & p) >> int(math.log2(p))
            if r:
                return Value.HIGH
            else:
                return Value.LOW

    def pin_polarity(self, pin, pola):
        pass

    def get_pins_mode(self, pin):
        pass



if __name__ == '__main__':
    # Create an object 
    dev = TCA9535()

    # Configure pin mode OUTPUT
    dev.pin_mode(Pin.P0_0, Mode.INPUT)
    # dev.pin_mode(Pin.P0_2, Mode.OUTPUT)
    # dev.pin_mode(Pin.P0_4, Mode.OUTPUT)
    # dev.pin_mode(Pin.P0_6, Mode.OUTPUT)
    # dev.pin_mode(Pin.P1_1, Mode.OUTPUT)
    # dev.pin_mode(Pin.P1_3, Mode.OUTPUT)
    # dev.pin_mode(Pin.P1_5, Mode.OUTPUT)
    # dev.pin_mode(Pin.P1_7, Mode.OUTPUT)

    # Configure pin mode INPUT
    # dev.pin_mode(Pin.P0_0, Mode.INPUT)
    # dev.pin_mode(Pin.P0_2, Mode.INPUT)
    # dev.pin_mode(Pin.P0_4, Mode.INPUT)
    # dev.pin_mode(Pin.P0_6, Mode.INPUT)
    # dev.pin_mode(Pin.P1_1, Mode.INPUT)
    # dev.pin_mode(Pin.P1_3, Mode.INPUT)
    # dev.pin_mode(Pin.P1_5, Mode.INPUT)
    # dev.pin_mode(Pin.P1_7, Mode.INPUT)

    # Digital write
    # dev.digital_write(Pin.P0_1, Value.HIGH)
    # time.sleep(1)
    # dev.digital_write(Pin.P0_1, Value.LOW)
    # time.sleep(1)

    # dev.digital_write(Pin.P1_1, Value.HIGH)
    # time.sleep(1)
    # dev.digital_write(Pin.P1_1, Value.LOW)
    # time.sleep(1)

    # Digital read
    print(dev.digital_read(Pin.P0_1))
    print(dev.digital_read(Pin.P1_1))