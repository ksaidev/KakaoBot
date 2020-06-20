class Writer:
    def __init__(self, crypto, StreamWriter):
        self.crypto=crypto
        self.StreamWriter=StreamWriter
        self.PacketID=0
    
    def __getPacketID(self):
        self.PacketID += 1
        return self.PacketID
    
    async def sendPacket(self, packet):
        packet.PacketID = self.__getPacketID()
        self.StreamWriter.write(packet.toEncryptedLocoPacket(self.crypto))
        await self.StreamWriter.drain()