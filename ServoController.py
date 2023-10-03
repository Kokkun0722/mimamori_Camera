from smbus import SMBus
import time
import numpy as np

class ServoController:
    def __init__(self, address,number):
        self.address = address
        self.i2cbus = SMBus(1)
        gain=number*5
        if(number==0):
            self.command=[0,1,2,3,4]
        elif(number==1):
            self.command=[5,6,7,8,9]

    def move(self, angle,delay=0.1):
        self.i2cbus.write_byte(self.address, self.command[angle])
        time.sleep(delay)

        
if __name__ == '__main__':
    left = ServoController(0x8,0)
    right = ServoController(0x8,1)
    
    for i in range(5):
        left.move(i)
        
