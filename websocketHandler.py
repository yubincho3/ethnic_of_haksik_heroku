import asyncio
import json

from restaurant import *

restaurantList = []

# 웹소켓 프로토콜을 통해 클라이언트의 요청을 처리하는 클래스입니다.
class WebsocketHandler:
    def __init__(self, websock):
        self.websock = websock

    # 웹소켓 연결을 종료합니다.
    def __del__(self):
        if not self.websock.closed:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.websock.close())
            loop.close()

    # 시간표 정보를 수신해서 먹을 수 있는 학식의 목록을 정리하고
    # 마크다운 문자열로 가공해서 클라이언트에게 전송합니다.
    async def handleTimeTable(self):
        jsonString = await self.websock.recv()
        unableTimes = [tuple(i) for i in json.loads(jsonString)]
        result = ''

        # 레스토랑 목록 순회
        for restaurant in restaurantList:
            menuStr = ''

            # 레스토랑의 코너 목록 순회
            for corner in restaurant.getCornerList():
                cornerMenu = corner.getAbleMenu(unableTimes)

                # 먹을 수 있는 메뉴가 있다면 결과 문자열에 추가합니다.
                if cornerMenu:
                    menuStr += f'#### {corner.name}\n'
                    menuStr += '\n'.join(map(str, cornerMenu)) + '\n'

            # 먹을 수 있는 메뉴가 존재하는 코너가 있다면 레스토랑의 이름도 추가합니다.
            if menuStr:
                restaurantName = f'## {Restaurants[restaurant.name].value}'
                result += f'{restaurantName}\n{menuStr}\n'

        await self.websock.send(result)

    # 클라이언트 핸들링을 시작합니다.
    async def startHandle(self):
        ip = self.websock.remote_address[0]
        print(f'connected: {ip}')

        try:
            while True:
                await self.handleTimeTable()
        except:
            print(f'disconnected: {ip}')

async def handler(websock):
    obj = WebsocketHandler(websock)
    await obj.startHandle()
