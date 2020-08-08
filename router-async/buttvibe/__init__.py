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
        """
        close connection to intiface
        """
        await self.bp_client.stop_scanning()
        await self.bp_client.disconnect()
        print('buttvibe disconnected, quitting')

    async def handle_command(self, command):
        if command['action'] == 'vibe':
            await self.set_vibe(command['level'])
        elif command['action'] == 'vibefor':
            await self.vibe_for(command['time'],command['level'])

    async def set_vibe(self, level):
        """
        send vibration level to buttplug

        :param level: vibration level to send to buttplug
        :type level: float
        """
        if 1 >= level > 0:
            logging.info(f'buttvibe sending level {level}')
            await self.bp_device.send_vibrate_cmd(level)
        else:
            await self.stop_vibe()

    async def stop_vibe(self):
        """
        send stop command to buttplug
        """
        logging.info(f'buttvibe sending stop')
        await self.bp_device.send_stop_device_cmd()

    async def vibe_for(self, ms, level):
        """
        vibrate buttplug for a certain number of milliseconds
        
        :param ms: milliseconds to wait
        :type level: int
        :param level: vibration level to send to buttplug
        :type level: float
        """
        await self.bp_device.send_vibrate_cmd(level)
        print("done")

        seconds = ms / 1000
        asyncio.get_event_loop().call_later(seconds, self.stop_vibe)

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

    async def _off_after(self, milliseconds):
        seconds = milliseconds / 1000
        await asyncio.sleep(seconds)
        await self.stop_vibe()
