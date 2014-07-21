import os
import logging


class Log(object):

    def __init__(self, name=''):
        
        logging.basicConfig(
                        filename='bmxtime.log',
                        level = logging.DEBUG,
                        format = '%(asctime)s - [%(levelname)-8s] - %(message)s',
                        datefmt = '%d.%m.%Y %H:%M:%S')
        self.logger = logging
        	
    def info(self, message):        
        self.logger.info(message)

    def error(self, message):        
        self.logger.error(message)

    def warning(self, message):        
        self.logger.warning(message)

    def debug(self, message):        
        self.logger.debug(message)

    def close(self, *args, **kwargs):
        logging.shutdown()
