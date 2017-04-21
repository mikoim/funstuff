import json
import logging

import re
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

from .plugin_loader import PluginLoader

__all__ = ['Room', 'Server']


class Room:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._clients = set()

    async def join(self, ws):
        """
        :type ws: WebSocketServerProtocol
        """

        self._logger.debug('join {:s}:{:d}'.format(*ws.remote_address))
        self._clients.add(ws)

    async def leave(self, ws):
        """
        :type ws: WebSocketServerProtocol
        """

        self._logger.debug('leave {:s}:{:d}'.format(*ws.remote_address))
        self._clients.remove(ws)

    async def say(self, message):
        """
        :type message: str
        """

        self._logger.debug('say "{:s}"'.format(message))
        for ws in self._clients:
            await ws.send(json.dumps({"data": message}))


class Server:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.room = Room()
        self.regexBot = re.compile('^bot (?P<plugin>\S+)( (?P<args>.*)|)')
        self.plugins = PluginLoader.get_plugins()

    def serve(self, host='0.0.0.0', port=8080):
        return websockets.serve(self.__gate, host, port)

    async def __gate(self, ws, _):
        await self.room.join(ws)

        while True:
            try:
                message = await ws.recv()
            except ConnectionClosed:
                break

            await self.room.say(message)

            match = self.regexBot.match(message)
            if match:
                try:
                    plugin = match.group('plugin')
                    if plugin not in self.plugins:
                        raise RuntimeError('unknown plugin')

                    args = match.group('args')
                    if args is None:
                        args = []
                    else:
                        args = args.split()

                    self._logger.debug('execute plugin "{:s}" [{:s}]'.format(plugin, ','.join(args)))

                    result = self.plugins[plugin].execute(args)
                except (ValueError, RuntimeError) as e:
                    result = str(e)
                finally:
                    await self.room.say(result)

        await self.room.leave(ws)
