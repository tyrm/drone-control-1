#!/usr/bin/env python

import asyncio
import json
import logging
from argparse import ArgumentParser

import websockets

from buttvibe import ButtVibe
from dcesp import DcEsp
from nipplevibe import NippleVibe

# Globals
CLIENTS = set()

# Init Stuff
parser = ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
parser.add_argument('-e', '--esp32', default='/dev/ttyUSB0', help='ESP32 serial')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)

logging.debug('starting')

# init esp
esp = DcEsp(args.esp32)

# init buttvibe
buttvibe = ButtVibe()

# init nipplevibes
nipplevibe = [NippleVibe(esp, 0), NippleVibe(esp, 1)]

async def register(websocket):
    CLIENTS.add(websocket)
    logging.debug(f'Registered client {websocket}')


async def unregister(websocket):
    CLIENTS.remove(websocket)
    logging.debug(f'Unregistered client {websocket}')


async def hander(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = None
            try:
                data = json.loads(message)
            except json.decoder.JSONDecodeError:
                pass

            for command in data:
                if command["device"] == "butt":
                    await buttvibe.handle_command(command)
                elif command["device"] == "nipple":
                    index = 0
                    try:
                        index = command["index"]
                    except KeyError:
                        pass

                    await nipplevibe[index].handle_command(command)
                elif command["device"] == "popper":
                    pass

    except websockets.exceptions.ConnectionClosedError:
        logging.warning('client unexpectedly closed the connection')
    finally:
        await unregister(websocket)


start_server = websockets.serve(hander, 'localhost', 6969)

asyncio.get_event_loop().run_until_complete(start_server)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print('Canceled')
