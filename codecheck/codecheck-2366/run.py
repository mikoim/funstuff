#!/usr/bin/env python3

import asyncio
import logging

from app import Server

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    loop = asyncio.get_event_loop()
    start_server = Server().serve()
    server = loop.run_until_complete(start_server)

    logger.info('subot started.')

    loop.run_forever()

    logger.info('subot stopped.')
