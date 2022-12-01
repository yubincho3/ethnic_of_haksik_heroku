import asyncio
import json

from restaurant import *

restaurantList = []

class WebsocketHandler:
    def __init__(self, websock):
        self.websock = websock

    async def startHandle(self):
        ip = self.websock.remote_address[0]
        print(f'connected: {ip}')

        try:
            while True:
                jsonString = await self.websock.recv()
                unableTimes = [tuple(i) for i in json.loads(jsonString)]
                result = ''

                for restaurant in restaurantList:
                    tempStr = ''

                    for corner in restaurant.getCornerList():
                        cornerMenu = corner.getAbleMenu(unableTimes)

                        if cornerMenu:
                            tempStr += f'#### {corner.name}\n'
                            tempStr += '\n'.join(map(str, cornerMenu)) + '\n'

                    if tempStr:
                        restaurantName = f'## {Restaurants[restaurant.name].value}'
                        result += f'{restaurantName}\n{tempStr}\n'

                await self.websock.send(result)
        except:
            print(f'disconnected: {ip}')

async def handler(websock):
    obj = WebsocketHandler(websock)
    await obj.startHandle()
