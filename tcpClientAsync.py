import asyncio
import pickle

PACKET_SIZE = 256

# 비동기적으로 TCP 통신을 수행하는 클래스입니다.
# 데이터의 송수신은 다음과 같은 과정으로 진행됩니다.
# 1. 먼저 보낼 데이터의 크기를 보낸다.
# 2. 데이터를 pickle 모듈의 dumps 함수를 사용해 bytes 타입으로 직렬화한다.
# 3. 직렬화한 데이터를 packetSize 만큼 잘라서 보낸다.
class TcpClientAsync:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.__reader = reader
        self.__writer = writer

    # 데이터를 비동기적으로 수신합니다.
    async def getDataAsync(self, packetSize: int = PACKET_SIZE):
        packet = b''

        dataSize = int.from_bytes(await self.__reader.read(packetSize))

        while dataSize > 0:
            packet += await self.__reader.read(min(dataSize, packetSize))
            dataSize -= packetSize

        return pickle.loads(packet)

    # 데이터를 비동기적으로 송신합니다.
    async def sendDataAsync(self, data, packetSize: int = PACKET_SIZE):
        packet = pickle.dumps(data)

        await self.__writer.drain()
        self.__writer.write(len(packet).to_bytes(packetSize))

        while packet:
            await self.__writer.drain()
            self.__writer.write(packet[:packetSize])
            packet = packet[packetSize:]
