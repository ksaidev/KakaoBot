import asyncio


class Writer:
    def __init__(self, crypto, StreamWriter, PacketDict):
        self.crypto = crypto
        self.StreamWriter = StreamWriter
        self.PacketID = 0
        self.PacketDict = PacketDict

    def __getPacketID(self):
        self.PacketID += 1
        return self.PacketID

    async def sendPacket(self, packet):
        pid = self.__getPacketID()

        fut = asyncio.get_event_loop().create_future()
        self.PacketDict[pid] = fut

        packet.PacketID = pid
        self.StreamWriter.write(packet.toEncryptedLocoPacket(self.crypto))
        await self.StreamWriter.drain()

        return await fut
