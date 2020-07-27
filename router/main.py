import kontrol2  # local
import popperpump  # local
import logging
import time
from argparse import ArgumentParser

# Init Stuff
parser = ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)

logging.info('Starting up')

if __name__ == "__main__":
    pump = popperpump.PopperPump()
    k2 = kontrol2.Kontrol2(pump)

    try:
        while True:
            time.sleep(100)
    except (Exception, KeyboardInterrupt):
        pass

    logging.debug("Closing")
    k2.close()
