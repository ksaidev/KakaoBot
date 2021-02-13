import asyncio
import packet
from bson import BSON as bson
import time
import json
import os
import httpApi
import hashlib
import requests


class Chat:
    def __init__(self, channel, body):
        self.channel = channel

        self.rawBody = body

        self.logId = self.rawBody["chatLog"]["logId"]

        self.type = self.rawBody["chatLog"]["type"]

        self.message = self.rawBody["chatLog"]["message"]

        self.msgId = self.rawBody["chatLog"]["msgId"]

        self.authorId = self.rawBody["chatLog"]["authorId"]

        try:
            if "attachment" in self.rawBody["chatLog"]:
                self.attachment = json.loads(
                    self.rawBody["chatLog"]["attachment"])
            else:
                self.attachment = {}
        except:
            pass

#       self.nickName = self.rawBody["authorNickname"] 현재 작동이 멈춘관계로 authorId로 대채

        self.nickName = self.rawBody["chatLog"]["authorId"]
        ########## NOT WORKING ##########
        """
    async def __uploadPicture(self, path, w, h):
        f = open(path, "rb")
        filedata = f.read()
        f.close()

        filehash = hashlib.sha1(filedata).hexdigest()

        shipRecv = (await self.channel.writer.sendPacket(packet.Packet(0, 0, "SHIP", 0, bson.encode({
            "c": self.chatId,
            "s": len(filedata),
            "t": 2,  # Photo
            "cs": filehash,
            "e": "jpg",
        })))).toJsonBody()

        host = shipRecv["vh"]
        port = shipRecv["p"]

        key = shipRecv["k"]

        cm = cryptoManager.CryptoManager()

        sock = socket.socket()
        sock.connect((host, port))

        sock.send(cm.getHandshakePacket())
        sock.send(packet.Packet(0, 0, "POST", 0, bson.encode({
            "u": self.authorId,
            "k": key,
            "t": 2,  # Photo
            "s": len(filedata),
            "c": self.chatId,
            "mid": self.authorId,
            "w": w,
            "h": h,
            "ns": False,
            "av": "8.9.1",
            "os": "android",
            "nt": 0,
            "mm": "",
            "ex": "{}",
        })).toEncryptedLocoPacket(cm))

        dataPacket = io.BytesIO()

        iv = os.urandom(16)
        enc = cm.aesEncrypt(filedata, iv)
        
        dataPacket.write(struct.pack("<I", len(enc)+len(iv)))
        dataPacket.write(iv)
        dataPacket.write(enc)

        sock.send(dataPacket.getvalue())
        
        d=sock.recv(1024)

        dataRecv = packet.Packet()
        dataRecv.readEncryptedLocoPacket(d, cm)

        body=dataRecv.toJsonBody()

        if body["status"] != 0:
            raise Exception("Image Upload Error: {}".format(body))

        return (key, filehash, len(filedata))
	"""

    async def reply(self, msg, t=1):
        return await self.channel.sendChat(msg, json.dumps({
            "attach_only": False,
            "attach_type": t,
            "mentions": [],
            "src_linkId": self.channel.li,
            "src_logId": self.logId,
            "src_mentions": [],
            "src_message": self.message,
            "src_type": self.type,
            "src_userId": self.authorId
        }), 26)

    async def sendChat(self, msg, extra, t):
        return await self.channel.sendChat(msg, extra, t)

    async def sendText(self, msg):
        return await self.channel.sendText(msg)

    async def delete(self):
        return await self.channel.deleteMessage(self.logId)

    async def hide(self):
        return await self.channel.hideMessage(self.logId, self.type)

    async def kick(self):
        return await self.channel.kickMember(self.authorId)

    async def sendPhoto(self, data, w, h):
        path, key, url = httpApi.upload(data, "image/jpeg", self.authorId)
        return await self.channel.forwardChat("", json.dumps({
            "thumbnailUrl": url,
            "thumbnailHeight": w,
            "thumbnailWidth": h,
            "url": url,
            "k": key,
            "cs": hashlib.sha1(data).hexdigest().upper(),
            "s": len(data),
            "w": w,
            "h": h,
            "mt": "image/jpeg"
        }), 2)

    async def sendPhotoPath(self, path, w, h):
        f = open(path, "rb")
        data = f.read()
        f.close()

        return await self.sendPhoto(data, w, h)

    async def sendPhotoUrl(self, url, w, h):
        r = requests.get(url)
        r.raise_for_status()

        return await self.sendPhoto(r.content, w, h)

    async def sendLongText(self, title, content):
        path, key, url = httpApi.upload(
            content.encode("utf-8"), "image/jpeg", self.authorId)

        return await self.channel.forwardChat(title, json.dumps({"path": path, "k": key, "s": len(content), "cs": "", "sd": True}), 1)
