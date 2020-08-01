import logging
from .kontrol2 import Kontrol2
from .errors import KontrolNotAttachedError, KontrolAlreadyAttachedError


class GenericKontrol:
    def __init__(self):
        self.kontrol = None
        self.channel = None

    def k_attach(self, channel, k: Kontrol2):
        if self.kontrol is None:
            self.kontrol = k
            self.channel = channel
            logging.debug(f'Attached on channel {channel}')
        else:
            raise KontrolAlreadyAttachedError(f'Cannot attach to channel {channel} already attached to {self.channel}')

    def k_button_down(self, button, ):
        if self.kontrol is not None:
            self.kontrol.k_led_on(self.channel, button)
            logging.debug(f'Pushed button {button}_{self.channel}')
        else:
            raise KontrolNotAttachedError(f'Not attached to Kontroller')

    def k_button_up(self, button):
        if self.kontrol is not None:
            self.kontrol.k_led_off(self.channel, button)
            logging.debug(f'Released button {button}_{self.channel}')
        else:
            raise KontrolNotAttachedError(f'Not attached to Kontroller')

    def k_knob(self, level):
        if self.kontrol is not None:
            logging.debug(f'Twisted knob {self.channel} to {level}')
        else:
            raise KontrolNotAttachedError(f'Not attached to Kontroller')

    def k_slider(self, level):
        if self.kontrol is not None:
            logging.debug(f'Slid slider {self.channel} to {level}')
        else:
            raise KontrolNotAttachedError(f'Not attached to Kontroller')
