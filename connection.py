# -*- coding: iso-8859-1 -*-

from __future__ import print_function

import os
import serial
import time
from datetime import timedelta

from serial.tools import list_ports
from logger import Log

log = Log(__name__)

class Connections(object):

    def __init__(self):

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        #self.ser.port = 8
        self.ser.timeout = 1
        
    def read_data(self, serial_ready, port=8):
        """
        Open a serial connection and wait until 3 times come data´s from serial port.
        After this the serial connection will be closed
        """
        
        log.info("Connect the Ardurino on port %s" %port)
        self.ser.port = port
        self.ser.open()
        i = 0
        f = open('temp', 'w')
        while( i < 3):
            time_data = self.ser.readline()
            time.sleep(1)
            if (time_data):
                time_data = int(time_data.rstrip())

                #convert the timedelta to human readable time
                time_data = str(timedelta(milliseconds=time_data))[2:-3]

                # pront data to temp
                print(time_data, file=f)
                log.debug(time_data)
                i = i + 1
                
        f.close()
        self.ser.close()
        log.info("Close serial connection with Ardurino")
        return
                
            
    def __del__(self):
        self.ser.close()
    
        
class Ports():

    def get_serial_ports(self):
        """
        Returns the port of ardurino
        """
        self.list = []
        
        for port in list_ports.comports():
            if "Arduino" in port[1]:
                log.info("Ardurino found on port %s" %(port[0]))
                self.list.append(port[0])

        return self.list



