from buttplug.client import (ButtplugClientWebsocketConnector, ButtplugClient,
                             ButtplugClientDevice, ButtplugClientConnectorError)
from buttplug.core import ButtplugLogLevel
import logging
import asyncio

class ButtVibe:
    def __init__(self):
        logging.debug("Buttvibe Started")

        self.program_running = False
        self.vibrate_level = 0

        self.buttplug_client = ButtplugClient("Drone Control 1")
        self.connector = ButtplugClientWebsocketConnector("ws://127.0.0.1:12345")

        #TODO init some stuff

    def is_program_running(self):
        return self.program_running

    def send_level(self, level):
        if level > 0:
            logging.error("I want to send a vibration level command to your buttplug.")
            #TODO send level command to buttplug
        else:
            logging.error("I want to send the stop command to your buttplug.")
            #TODO send level command to

    def set_level(self, level):
        float_level = round(level/127, 2)
        logging.debug("Setting butt vibration level to: {}".format(float_level))
        self.vibrate_level = float_level

        if self.program_running:
            self.send_level(float_level)

    def start_program(self):
        logging.debug("starting butt vibration")
        self.send_level(self.vibrate_level)
        self.program_running = True

    def start_single(self):
        if not self.program_running:
            # send vibe
            logging.debug("starting single butt vibration")
            self.send_level(self.vibrate_level)
            return True
        else:
            # mute
            logging.debug("starting single butt mute")
            self.send_level(0)
            return False

    def stop_program(self):
        logging.debug("stopping butt vibration")
        self.send_level(0)
        self.program_running = False

    def stop_single(self):
        if not self.program_running:
            # stop vibe
            logging.debug("stopping single butt vibration")
            self.send_level(0)
            return False
        else:
            # unmute
            logging.debug("stopping single butt mute")
            self.send_level(self.vibrate_level)
            return True
