#!/usr/bin/env python

import asyncio
import json
import logging
import websockets
from argparse import ArgumentParser

from buttvibe import ButtVibe

# Init Stuff
parser = ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)

# Globals
CLIENTS = set()


async def register(websocket):
    CLIENTS.add(websocket)
    logging.debug(f'Registered client {websocket}')


async def unregister(websocket):
    CLIENTS.remove(websocket)
    logging.debug(f'Unregistered client {websocket}')


async def hander(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            data = None
            try:
                data = json.loads(message)
            except json.decoder.JSONDecodeError:
                pass

            print(data[0])
    except websockets.exceptions.ConnectionClosedError:
        logging.warning('client unexpectedly closed the connection')
    finally:
        await unregister(websocket)


if __name__ == '__main__':
    logging.debug('starting')

    # init buttvibe
    buttvibe = ButtVibe()

    start_server = websockets.serve(hander, 'localhost', 6969)

    asyncio.get_event_loop().run_until_complete(start_server)

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('Canceled')
