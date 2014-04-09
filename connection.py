import os
import serial
from serial.tools import list_ports


class Connections():
    
        
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

    def connect(self):
        return True


