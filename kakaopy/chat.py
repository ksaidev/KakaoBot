from .http_api import upload

import json
import hashlib
import requests


class Chat:
    def __init__(self, channel, body):
        self.channel = channel
        self.body = body
        self.log_id = self.body["chatLog"]["logId"]
        self.type = self.body["chatLog"]["type"]
        self.message = self.body["chatLog"]["message"]
        self.msg_id = self.body["chatLog"]["msgId"]
        self.author_id = self.body["chatLog"]["authorId"]

        if "attachment" in self.body["chatLog"]:
            self.attachment = json.loads(
                self.body["chatLog"]["attachment"])
        else:
            self.attachment = {}


    async def reply(self, msg, t=1):
        return await self.channel.send_chat(msg, json.dumps({
            "attach_only": False,
            "attach_type": t,
            "mentions": [],
            "src_linkId": self.channel.li,
            "src_logId": self.log_id,
            "src_mentions": [],
            "src_message": self.message,
            "src_type": self.type,
            "src_userId": self.author_id
        }), 26)

    async def send_chat(self, msg, extra, t):
        return await self.channel.send_chat(msg, extra, t)

    async def send_text(self, msg):
        return await self.channel.send_text(msg)

    async def delete(self):
        return await self.channel.delete_message(self.log_id)

    async def hide(self):
        return await self.channel.hide_message(self.log_id, self.type)

    async def kick(self):
        return await self.channel.kick_member(self.author_id)

    async def send_photo(self, data, w, h):
        path, key, url = upload(data, "image/jpeg", self.author_id)
        return await self.channel.forward_chat("", json.dumps({
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

    async def send_photo_by_path(self, path, w, h):
        with open(path, "rb") as f:
            data = f.read()

        return await self.send_photo(data, w, h)

    async def send_photo_by_url(self, url, w, h):
        r = requests.get(url)
        r.raise_for_status()

        return await self.send_photo(r.content, w, h)

    async def send_long_text(self, title, content):
        path, key, url = upload(content.encode(
            "utf-8"), "image/jpeg", self.author_id)

        return await self.channel.forward_chat(title, json.dumps(
            {"path": path, "k": key, "s": len(content), "cs": "", "sd": True}), 1)
