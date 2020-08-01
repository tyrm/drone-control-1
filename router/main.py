import logging
import time
from argparse import ArgumentParser

import toycomms
from buttvibe import ButtVibe
from kontrol2 import Kontrol2, GenericKontrol

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
    toycomms = toycomms.ToyComms()
    k2 = Kontrol2(args.kontrol)

    buttvibe = ButtVibe()
    k2.attach(0, buttvibe)
    k2.attach(1, GenericKontrol())
    k2.attach(2, GenericKontrol())
    k2.attach(3, GenericKontrol())
    k2.attach(4, GenericKontrol())
    k2.attach(5, GenericKontrol())
    k2.attach(6, GenericKontrol())
    k2.attach(7, GenericKontrol())

    try:
        while True:
            time.sleep(100)
    except (Exception, KeyboardInterrupt):
        pass

    logging.debug("Closing")
    k2.close()
