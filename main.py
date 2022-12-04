#!/usr/bin/env python
import asyncio
import signal
import os

import websocketHandler
import websockets

from menuCrawler import crawlThisWeeksMenu

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    websocketHandler.restaurantList = crawlThisWeeksMenu()

    async with websockets.serve(
        websocketHandler.handler,
        host = '',
        #port = int(os.environ['PORT'])
        port=26656
    ):
        await stop

if __name__ == '__main__':
    asyncio.run(main())
    print('server stopped.')
