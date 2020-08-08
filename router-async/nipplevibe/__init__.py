import logging
import asyncio

from dcesp import DcEsp

class NippleVibe:
    def __init__(self, esp: DcEsp, channel):
        self.esp = esp
        self.vib_chan = channel

        self.running = False
        self.level = 0

    async def handle_command(self, command):
        if command['action'] == 'vibe':
            if 1 >= command['level'] > 0:
                self.set_vibe(command['level'])
            else:
                self.stop_vibe()
        elif command['action'] == 'vibefor':
            self.vibe_for(command['time'], command['level'])

    def is_running(self):
        return self.running

    def set_vibe(self, level):
        self._send_level(level)

    def stop_vibe(self):
        self._send_level(0)

    def vibe_for(self, ms, level):
        self.set_vibe(level)

        seconds = ms / 1000
        asyncio.get_event_loop().call_later(seconds, self.stop_vibe)

    # Private Functions
    def _send_level(self, level):
        int_level = int(255 * level)
        self.esp.vibrate(self.vib_chan, int_level)