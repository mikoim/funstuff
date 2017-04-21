#!/usr/bin/env python3

import asyncio
from threading import Thread

from bottle import static_file, route, run

from app import Server


def serve_web():
    while True:
        @route('/')
        def index():
            static_file('index.css', root='./app')
            static_file('client.js', root='./app')
            return static_file("index.html", root='./app')

        @route('/<filename>')
        def server_static(filename):
            return static_file(filename, root='./app')

        run(host='localhost', port=9000)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_server = Server().serve('localhost')
    server = loop.run_until_complete(start_server)

    t = Thread(target=serve_web)
    t.daemon = True
    t.start()

    loop.run_forever()
