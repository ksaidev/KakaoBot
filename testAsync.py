import asyncio
import time


class Client:
    async def __recvPacket(self):
        while True:
            await asyncio.sleep(1)
            print("running")

    async def __heartbeat(self):
        while True:
            await asyncio.sleep(5)
            print("heartbeat")

    def login(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__recvPacket())
        self.loop.create_task(self.__heartbeat())
        self.loop.run_forever()


client = Client()
client.login()
