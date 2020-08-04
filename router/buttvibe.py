import logging
import asyncio
import threading

from buttplug.client import (ButtplugClientWebsocketConnector, ButtplugClient,
                             ButtplugClientDevice, ButtplugClientConnectorError)
import util
from kontrol2 import Kontrol2, KontrolAlreadyAttachedError, KontrolNotAttachedError


class ButtVibe:
    def __init__(self):
        self.running = False
        self.level = 0
        self.last_sent_level = 0

        # Required for Kontroller
        self.kontrol = None
        self.channel = None

        # Buttplug Client
        self.bp_client = ButtplugClient("Drone Control 1")
        self.bp_connector = ButtplugClientWebsocketConnector("ws://127.0.0.1:12345")
        self.bp_device = None

        threading.Thread(target=self._init_buttplug_client_thread, daemon=True).start()

        logging.debug("Buttvibe Started")

    def is_running(self):
        return self.running

    def set_level(self, level):
        logging.debug("Setting butt vibration level to: {}".format(round(level, 2)))
        self.level = level

        if self.running:
            self._send_level(level)

    def start_vibe(self):
        logging.debug("starting butt vibration")
        self._send_level(self.level)
        self.running = True

    def start_single(self):
        if not self.running:
            # send vibe
            logging.debug("starting single butt vibration")
            self._send_level(self.level)
            self.kontrol.k_led_on(self.channel, 's')
        else:
            # mute
            logging.debug("starting single butt mute")
            self._send_level(0)
            self.kontrol.k_led_off(self.channel, 's')

    def stop_vibe(self):
        logging.debug("stopping butt vibration")
        self._send_level(0)
        self.running = False

    def stop_single(self):
        if not self.running:
            # stop vibe
            logging.debug("stopping single butt vibration")
            self._send_level(0)
            self.kontrol.k_led_off(self.channel, 's')
        else:
            # unmute
            logging.debug("stopping single butt mute")
            self._send_level(self.level)
            self.kontrol.k_led_on(self.channel, 's')

    # Private Functions
    async def _cancel_me(self):
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass

    def _device_added(self, emitter, dev: ButtplugClientDevice):
        logging.debug(f'Buttvibe device added: {dev}')
        self.bp_device = dev
        asyncio.create_task(self._device_added_task(self.bp_device))

    async def _device_added_task(self, dev: ButtplugClientDevice):
        if "VibrateCmd" in dev.allowed_messages.keys():
            await dev.send_vibrate_cmd(0.5)
            await asyncio.sleep(1)
            await dev.send_stop_device_cmd()

    def _device_removed(self, emitter, dev: ButtplugClientDevice):
        logging.debug(f'Buttvibe device removed: {dev}')
        self.bp_device = None

    async def _init_buttplug_client(self):
        self.bp_client.device_added_handler += self._device_added
        self.bp_client.device_removed_handler += self._device_removed

        try:
            await self.bp_client.connect(self.bp_connector)
        except ButtplugClientConnectorError as e:
            print("Could not connect to server, exiting: {}".format(e.message))
            return


        await self.bp_client.start_scanning()

        self.bp_loop = asyncio.get_event_loop()

        task = asyncio.create_task(self._cancel_me())
        try:
            await task
        except asyncio.CancelledError:
            pass

        await self.bp_client.stop_scanning()

        await self.bp_client.disconnect()
        print("Disconnected, quitting")

    def _init_buttplug_client_thread(self):
        asyncio.run(self._init_buttplug_client(), debug=True)

    def _send_level(self, level):
        if level > 0:
            logging.debug(f'Sending level {level} to ButtVibe')
            if level != self.last_sent_level:
                asyncio.run_coroutine_threadsafe(self.bp_device.send_vibrate_cmd(level), self.bp_loop)
                self.last_sent_level = level
        else:
            logging.debug(f'Sending stop to ButtVibe')
            if level != self.last_sent_level:
                asyncio.run_coroutine_threadsafe(self.bp_device.send_stop_device_cmd(), self.bp_loop)
                self.last_sent_level = level

    # Kontrol Functions
    def k_attach(self, channel, k: Kontrol2):
        if self.kontrol is None:
            self.kontrol = k
            self.channel = channel
            logging.debug(f'Buttvibe attached on channel {channel}')
        else:
            raise KontrolAlreadyAttachedError(f'Cannot attach to channel {channel} already attached to {self.channel}')

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
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_button_up(self, button):
        if self.kontrol is not None:
            if button == 's':
                self.stop_single()
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_knob(self, level):
        if self.kontrol is not None:
            pass  # not used
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')

    def k_slider(self, level):
        if self.kontrol is not None:
            float_level = round(util.scale(level, (0, 127), (0, 1)), 1)
            self.set_level(float_level)
        else:
            raise KontrolNotAttachedError(f'Buttvibe not attached to Kontroller')
