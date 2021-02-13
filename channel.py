import time

import packet
import bson


class Channel:
    def __init__(self, chatId, li, writer):
        self.chatId = chatId
        self.li = li
        self.writer = writer

    async def sendChat(self, msg, extra, t):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "WRITE", 0, bson.encode({
                "chatId": self.chatId,
                "extra": extra,
                "type": t,
                "msgId": time.time(),
                "msg": str(msg),
                "noSeen": False,
                })))).toJsonBody()

    async def forwardChat(self, msg, extra, t):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "FORWARD", 0, bson.encode({
                "chatId": self.chatId,
                "extra": extra,
                "type": t,
                "msgId": time.time(),
                "msg": str(msg),
                "noSeen": False,
                })))).toJsonBody()

    async def sendText(self, msg):
        return await self.sendChat(msg, "{}", 1)

    async def deleteMessage(self, logId):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "DELETEMSG", 0, bson.encode({
                "chatId": self.chatId,
                "logId": logId
                })))).toJsonBody()

    async def hideMessage(self, logId, t):
        if self.li:
            return (await self.writer.sendPacket(packet.Packet(0, 0, "REWRITE", 0, bson.encode({
                "c": self.chatId,
                "li": self.li,
                "logId": logId,
                "t": t
            })))).toJsonBody()

    async def kickMember(self, mid):
        if self.li:
            await (self.writer.sendPacket(packet.Packet(0, 0, "KICKMEM", 0, bson.encode({
                "li": self.li,
                "c": self.chatId,
                "mid": mid,
            })))).toJsonBody()

    async def setMeta(self, t, content):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "SETMETA", 0, bson.encode({
                "chatId": self.chatId,
                "type": t,
                "content": content
                })))).toJsonBody()

    async def getLinkInfo(self):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "INFOLINK", 0, bson.encode({
                "lis": [self.li]
                })))).toJsonBody()

    async def getChatInfo(self):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "CHATINFO", 0, bson.encode({
                "chatId": self.chatId
                })))).toJsonBody()

    async def getUserInfo(self, userId):
        return (await self.writer.sendPacket(packet.Packet(0, 0, "MEMBER", 0, bson.encode({
                "chatId": self.chatId,
                "memberIds": [userId]
                })))).toJsonBody()
