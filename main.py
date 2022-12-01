import asyncio
import signal
import os


import websocketHandler
import websockets

# --- 크롤러 모듈 --- #
from menuCrawler import crawlThisWeeksMenu

async def main():
    websocketHandler.restaurantList = crawlThisWeeksMenu()

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    #loop.add_signal_handler(signal.SIGTERM, stop.set_result)

    async with websockets.serve(  # type: ignore
        websocketHandler.handler,
        host = '',
        #port = int(os.environ['PORT'])
        port = 26656
    ):
        await stop

if __name__ == '__main__':
    asyncio.run(main())
