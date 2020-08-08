import logging
import asyncio

from buttplug.client import (ButtplugClientWebsocketConnector, ButtplugClient,
                             ButtplugClientDevice, ButtplugClientConnectorError)


class ButtVibe:
    def __init__(self):
        self.running = False
        self.level = 0
        self.last_sent_level = 0

        # Buttplug Client
        self.bp_client = ButtplugClient('Drone Control 1')
        self.bp_connector = ButtplugClientWebsocketConnector('ws://127.0.0.1:12345')
        self.bp_device = None

        self.bp_client.device_added_handler += self._device_added
        self.bp_client.device_removed_handler += self._device_removed

        asyncio.get_event_loop().run_until_complete(self._init_buttplug_client())

    async def close(self):
        await self.bp_client.stop_scanning()
        await self.bp_client.disconnect()
        print('buttvibe disconnected, quitting')

    # Private Functions
    def _device_added(self, emitter, dev: ButtplugClientDevice):
        logging.debug(f'buttvibe device added: {dev}')
        self.bp_device = dev
        asyncio.create_task(self._device_added_task(self.bp_device))

    async def _device_added_task(self, dev: ButtplugClientDevice):
        if "VibrateCmd" in dev.allowed_messages.keys():
            await dev.send_vibrate_cmd(0.5)
            await asyncio.sleep(1)
            await dev.send_stop_device_cmd()

    def _device_removed(self, emitter, dev: ButtplugClientDevice):
        logging.debug(f'buttvibe device removed: {dev}')
        self.bp_device = None

    async def _init_buttplug_client(self):
        logging.debug("buttvibe connecting to intiface")
        try:
            await self.bp_client.connect(self.bp_connector)
        except ButtplugClientConnectorError as e:
            logging.error(f'Could not connect to server, exiting: {e.message}')
            return

        logging.debug("buttvibe starting scan")
        await self.bp_client.start_scanning()
