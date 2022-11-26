import asyncio
from server import ClientHandler, handler

from menuCrawler import crawlThisWeeksMenu

CRAWL_URL = 'https://www.kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do'
HOST = '127.0.0.1'
PORT = 26656

async def main():
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    ClientHandler.restaurantList = crawlThisWeeksMenu(CRAWL_URL)
    asyncio.run(main())
