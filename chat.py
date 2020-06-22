import asyncio
import packet
from bson import BSON as bson
import time
class Chat:
    def __init__(self, writer, packet):
        self.writer = writer
        self.rawBody = packet.toJsonBody()

        self.chatId = self.rawBody["chatLog"]["chatId"]
        self.logId = self.rawBody["chatLog"]["logId"]

        self.type = self.rawBody["chatLog"]["type"]
        self.message = self.rawBody["chatLog"]["message"]

        if "attachment" in self.rawBody["chatLog"]:
            self.attachment = self.rawBody["chatLog"]["attachment"]
        self.nickName = self.rawBody["authorNickname"]

    async def reply(self, msg, extra = "{}", t = 1):
        return await self.writer.sendPacket(packet.Packet(0, 0, "WRITE", 0, bson.encode({
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": int(time.time()/10),
            "msg": msg,
            "noSeen": False,
        })))
        
    async def delete(self):
        await self.writer.sendPacket(packet.Packet(0, 0, "DELETEMSG", 0, bson.encode({
            "chatId":self.chatId,
            "logId":self.logId
        })))
        
    async def hide(self):
        if self.li:
            await self.writer.sendPacket(packet.Packet(0, 0, "REWRITE", 0, bson.encode({
                "c":chat.chatId,
                "li":chat.li,
                "logId":chat.logId,
                "t":1
            })))
