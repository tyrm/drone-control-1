import logging

from buttplug.client import (ButtplugClient, ButtplugClientWebsocketConnector)

import util
from kontrol2 import Kontrol2, KontrolAlreadyAttachedError, KontrolNotAttachedError


class ButtVibe:
    def __init__(self):
        self.running = False
        self.level = 0

        self.kontrol = None
        self.channel = None

        self.bp_client = ButtplugClient("Drone Control 1")
        self.bp_connector = ButtplugClientWebsocketConnector("ws://127.0.0.1:12345")

        # TODO init some stuff

        logging.debug("Buttvibe Started")

    def is_running(self):
        return self.running

    def set_level(self, level):
        float_level = util.scale(level, (0, 127), (0, 1))
        logging.debug("Setting butt vibration level to: {}".format(round(float_level, 2)))
        self.level = float_level

        if self.running:
            self._send_level(float_level)

    def start_vibe(self):
        logging.debug("starting butt vibration")
        self._send_level(self.level)
        self.running = True

    def start_single(self):
        if not self.running:
            # send vibe
            logging.debug("starting single butt vibration")
            self._send_level(self.level)
            return True
        else:
            # mute
            logging.debug("starting single butt mute")
            self._send_level(0)
            return False

    def stop_vibe(self):
        logging.debug("stopping butt vibration")
        self._send_level(0)
        self.running = False

    def stop_single(self):
        if not self.running:
            # stop vibe
            logging.debug("stopping single butt vibration")
            self._send_level(0)
            return False
        else:
            # unmute
            logging.debug("stopping single butt mute")
            self._send_level(self.level)
            return True

    # Private Functions
    def _send_level(self, level):
        if level > 0:
            logging.error("I want to send a vibration level command to your buttplug.")
            # TODO send level command to buttplug
        else:
            logging.error("I want to send the stop command to your buttplug.")
            # TODO send level command to

    # Kontrol Functions
    def k_attach(self, channel, k: Kontrol2):
        if self.kontrol is None:
            self.kontrol = k
            self.channel = channel
            logging.debug(f'Buttvibe on channel {channel}')
        else:
            raise KontrolAlreadyAttachedError(f'Cannot attach to channel {channel} already attached to {self.channel}')

    def k_button_down(self, button, ):
        if self.kontrol is not None:
            self.kontrol.k_led_on(self.channel, button)
            logging.debug(f'Pushed button {button}_{self.channel}')
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_button_up(self, button):
        if self.kontrol is not None:
            self.kontrol.k_led_off(self.channel, button)
            logging.debug(f'Released button {button}_{self.channel}')
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_knob(self, level):
        if self.kontrol is not None:
            pass  # not used
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_slider(self, level):
        if self.kontrol is not None:
            logging.debug(f'Slid slider {self.channel} to {level}')
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')
