import logging
import util

from dcesp import DcEsp
from kontrol2 import Kontrol2, KontrolAlreadyAttachedError, KontrolNotAttachedError


class NippleVibe:
    def __init__(self, esp: DcEsp, channel):
        self.esp = esp
        self.vib_chan = channel

        self.running = False
        self.level = 0

        # Required for Kontroller
        self.kontrol = None
        self.channel = None

    def is_running(self):
        return self.running

    def set_level(self, level):
        logging.debug(f'Setting nipple {self.vib_chan} vibration level to: {round(level, 2)}')
        self.level = level

        if self.running:
            self._send_level(level)

    def start_vibe(self):
        logging.debug(f'starting nipple {self.vib_chan} vibration')
        self._send_level(self.level)
        self.running = True

    def start_single(self):
        if not self.running:
            # send vibe
            logging.debug(f'starting single nipple {self.vib_chan} vibration')
            self._send_level(self.level)
            self.kontrol.k_led_on(self.channel, 's')
        else:
            # mute
            logging.debug(f'starting single nipple {self.vib_chan} mute')
            self._send_level(0)
            self.kontrol.k_led_off(self.channel, 's')

    def stop_vibe(self):
        logging.debug(f'stopping nipple {self.vib_chan} vibration')
        self._send_level(0)
        self.running = False

    def stop_single(self):
        if not self.running:
            # stop vibe
            logging.debug(f'stopping single nipple {self.vib_chan} vibration')
            self._send_level(0)
            self.kontrol.k_led_off(self.channel, 's')
        else:
            # unmute
            logging.debug(f'stopping single nipple {self.vib_chan} mute')
            self._send_level(self.level)
            self.kontrol.k_led_on(self.channel, 's')

    # Private Functions
    def _send_level(self, level):
        self.esp.vibrate(self.vib_chan, level)

    # Kontrol Functions
    def k_attach(self, channel, k: Kontrol2):
        if self.kontrol is None:
            self.kontrol = k
            self.channel = channel
            logging.debug(f'Nipple {self.vib_chan} attached on channel {channel}')
        else:
            raise KontrolAlreadyAttachedError(f'cannot attach to channel {channel} already attached to {self.channel}')

    def k_button_down(self, button):
        if self.kontrol is not None:
            if button == 'r':
                if self.is_running():
                    self.stop_vibe()
                    self.kontrol.k_led_off(self.channel, 's')
                    self.kontrol.k_led_off(self.channel, 'r')
                else:
                    self.start_vibe()
                    self.kontrol.k_led_on(self.channel, 's')
                    self.kontrol.k_led_on(self.channel, 'r')
            if button == 's':
                self.start_single()
        else:
            raise KontrolNotAttachedError(f'not attached to Kontroller')

    def k_button_up(self, button):
        if self.kontrol is not None:
            if button == 's':
                self.stop_single()
        else:
            raise KontrolNotAttachedError(f'not attached to Kontroller')

    def k_knob(self, level):
        if self.kontrol is not None:
            pass # Unused
        else:
            raise KontrolNotAttachedError(f'not attached to Kontroller')

    def k_slider(self, level):
        if self.kontrol is not None:
            float_level = int(util.scale(level, (0, 127), (0, 255)))
            self.set_level(float_level)
        else:
            raise KontrolNotAttachedError(f'NippleVibe {self.vib_chan} not attached to Kontroller')
