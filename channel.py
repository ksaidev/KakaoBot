import time

import packet
import bson


class Channel:
    def __init__(self, chatId, li, writer):
        self.chatId = chatId
        self.li = li
        self.writer = writer

    async def sendPacket(self, command, data):
        packet = packet.Packet(0, 0, command, 0, bson.encode(data))
        return (await self.writer.sendPacket(packet)).toJsonBody()

    async def sendChat(self, msg, extra, t):
        data = {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False,
        }
        return await self.sendPacket("WRITE", data)

    async def sendText(self, msg):
        return await self.sendChat(msg, "{}", 1)

    async def forwardChat(self, msg, extra, t):
        data = {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False,
        }
        return await self.sendPacket("FORWARD", data)

    async def deleteMessage(self, logId):
        data = {"chatId": self.chatId, "logId": logId}
        return await self.sendPacket("DELETEMSG", data)

    async def hideMessage(self, logId, t):
        if self.li:
            data = {
                "c": self.chatId,
                "li": self.li,
                "logId": logId,
                "t": t
            }
            return await self.sendPacket("REWRITE", data)

    async def kickMember(self, mid):
        if self.li:
            data = {
                "li": self.li,
                "c": self.chatId,
                "mid": mid,
            }
            await self.sendPacket("KICKMEM", data)

    async def setMeta(self, t, content):
        data = {
            "chatId": self.chatId,
            "type": t,
            "content": content
        }
        return await self.sendPacket("SETMETA", data)

    async def getLinkInfo(self):
        return await self.sendPacket("INFOLINK", {"lis": [self.li]})

    async def getChatInfo(self):
        return await self.sendPacket("CHATINFO", {"chatId": self.chatId})

    async def getUserInfo(self, userId):
        return await self.sendPacket("MEMBER", {"chatId": self.chatId, "memberIds": [userId]})
