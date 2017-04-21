import asyncio
import json

import re
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import *

from .bot import Bot

__all__ = ['Room', 'Server']


class Room:
    def __init__(self):
        self._clients = set()

    def join(self, ws):
        """
        :type ws: WebSocketServerProtocol
        """

        print('join: ', ws.remote_address)
        self._clients.add(ws)

    def leave(self, ws):
        """
        :type ws: WebSocketServerProtocol
        """

        print('leave: ', ws.remote_address)
        self._clients.remove(ws)

    @asyncio.coroutine
    def say(self, message):
        """
        :type message: str
        """

        print('say: ', message)
        for ws in self._clients:
            yield from ws.send(json.dumps({"data": message}))


class Server:
    def __init__(self):
        self.room = Room()
        self.regexBot = re.compile('^bot (?P<command>\S+) (?P<data>\S+)')

    def serve(self, host='localhost', port=3000):
        return websockets.serve(self.__gate, host, port)

    @asyncio.coroutine
    def __gate(self, ws, _):
        self.room.join(ws)

        while True:
            try:
                message = yield from ws.recv()
            except ConnectionClosed:
                break

            yield from self.room.say(message)

            match = self.regexBot.match(message)
            if match:
                yield from self.room.say(Bot(match.group('command'), match.group('data')).hash)

        self.room.leave(ws)
