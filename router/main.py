import logging
import time
from argparse import ArgumentParser

import serial

import buttvibe
import kontrol2
import popperpump

# Init Stuff
parser = ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
parser.add_argument('-e', '--esp32', default='/dev/tytyUSB0', help='ESP32 serial')
parser.add_argument('-k', '--kontrol', default='nanoKONTROL2:nanoKONTROL2 MIDI 1 32:0', help='MIDI port name')
parser.add_argument('-p', '--phidget', default=520822, type=int, help='Phidget serial')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)

logging.info('Starting up')

if __name__ == "__main__":
    esp32 = serial.Serial('/dev/ttyUSB0')  # open serial port
    logging.debug("opened serial port {}".format(esp32.name))

    butt = buttvibe.ButtVibe()
    pump = popperpump.PopperPump(args.phidget)

    k2 = kontrol2.Kontrol2(args.kontrol, butt, pump)

    try:
        while True:
            time.sleep(100)
    except (Exception, KeyboardInterrupt):
        pass

    logging.debug("Closing")
    k2.close()
