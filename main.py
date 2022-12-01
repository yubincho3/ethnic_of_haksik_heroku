#!/usr/bin/env python
import asyncio
import signal
import os

import websocketHandler
import websockets

# 크롤러 모듈
from menuCrawler import crawlThisWeeksMenu

async def main():
    websocketHandler.restaurantList = crawlThisWeeksMenu()

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result)

    async with websockets.serve(
        websocketHandler.handler,
        host = '',
        port = int(os.environ['PORT'])
    ):
        await stop

if __name__ == '__main__':
    asyncio.run(main())
