import threading

import serial
import logging


class DcEsp:
    def __init__(self, serial_port):
        logging.debug('Opening ToyComms')

        self.send_lock = threading.Lock()

        self.port = serial.Serial(serial_port, 115200)  # open serial port
        logging.debug(f'opened serial port {self.port.name}')

    def vibrate(self, channel, level):
        send_string = f'VIB,{channel},{level}\n'

        with self.send_lock:
            self.port.write(send_string.encode('utf_8'))
            logging.debug(f'toycomms sent {send_string}')
