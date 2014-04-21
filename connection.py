import os
import serial
import time
from serial.tools import list_ports

import __init__

class Connections():

    def __init__(self):

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = 8
        self.ser.timeout = 1
        if self.ser.isOpen():
            self.ser.close()
        
    def read_data(self, serial_ready):

        self.ser.open()
        i = 0
        while serial_ready:
            time_data = self.ser.read()
            print(time_data)
            if (i < 10):
                i =+ 1
                time.sleep(1)
                
            
    def __del__(self):
        self.ser.close()
    
        
class Ports():

    def get_serial_ports(self):
        """
        Returns a generator for all available serial ports
        """
        self.list = []
        if os.name == 'nt':
            # windows
            for i in range(25):
                try:
                    s = serial.Serial(i)
                    s.close()

                    self.list.append('COM' + str(i + 1))
                    
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                self.list.append(port[0])

        return self.list



