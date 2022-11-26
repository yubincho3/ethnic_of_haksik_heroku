# --- 네트워크 모듈 --- #
from tcpClientAsync import TcpClientAsync

# --- 코루틴 모듈 --- #
import asyncio

# --- 사용자 정의 모듈 --- #
from restaurant import *

class ClientHandler:
    restaurantList: list[Restaurant]

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.client = TcpClientAsync(reader, writer)

        info = writer.get_extra_info('peername')
        print(f'connected: {info[0]}:{info[1]}')

    # 클라이언트의 시간표를 전송받고 가능한 메뉴를 문자열로 송신합니다.
    async def menuHandler(self):
        unableTimes = await self.client.getDataAsync()
        result = ''

        for restaurant in self.restaurantList:
            tempStr = ''

            for corner in restaurant.getCornerList():
                cornerMenu = corner.getAbleMenu(unableTimes)

                if cornerMenu:
                    tempStr += corner.name + '\n'
                    tempStr += '\n'.join(map(str, cornerMenu)) + '\n'

            if tempStr:
                result += f'{restaurant.name}\n{tempStr}'

        await self.client.sendDataAsync(result)

    async def startHandle(self):
        while True:
            await self.menuHandler()

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    clientHandler = ClientHandler(reader, writer)
    await clientHandler.startHandle()
