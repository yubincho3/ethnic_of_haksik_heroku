import json

from restaurant import *

restaurantList = []

async def handler(websock):
    while True:
        jsonString = await websock.recv()
        unableTimes = [tuple(i) for i in json.loads(jsonString)]
        result = ''

        for restaurant in restaurantList:
            tempStr = ''

            for corner in restaurant.getCornerList():
                cornerMenu = corner.getAbleMenu(unableTimes)

                if cornerMenu:
                    tempStr += corner.name + '\n'
                    tempStr += '\n'.join(map(str, cornerMenu)) + '\n'

            if tempStr:
                result += f'{restaurant.name}\n{tempStr}'

        await websock.send(result)
