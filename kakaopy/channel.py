from .packet import Packet

import time
import bson


class Channel:
    def __init__(self, chat_id, li, writer):
        self.chat_id = chat_id
        self.li = li
        self.writer = writer

    async def __send_packet(self, command, data):
        packet = Packet(0, 0, command, 0, bson.encode(data))
        return (await self.writer.send_packet(packet)).to_json_body()

    async def send_chat(self, msg, extra, t):
        data = {
            "chatId": self.chat_id,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False,
        }
        return await self.__send_packet("WRITE", data)

    async def send_text(self, msg):
        return await self.send_chat(msg, "{}", 1)

    async def forward_chat(self, msg, extra, t):
        data = {
            "chatId": self.chat_id,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False,
        }
        return await self.__send_packet("FORWARD", data)

    async def read_message(self, log_id):
        data = {"chatId": self.chat_id, "watermark": log_id}
        return await self.__send_packet("NOTIREAD", data)

    async def delete_message(self, log_id):
        data = {"chatId": self.chat_id, "logId": log_id}
        return await self.__send_packet("DELETEMSG", data)

    async def hide_message(self, log_id, t):
        if self.li:
            data = {
                "c": self.chat_id,
                "li": self.li,
                "logId": log_id,
                "t": t
            }
            return await self.__send_packet("REWRITE", data)

    async def kick_member(self, mid):
        if self.li:
            data = {
                "li": self.li,
                "c": self.chat_id,
                "mid": mid,
            }
            await self.__send_packet("KICKMEM", data)

    async def set_meta(self, t, content):
        data = {
            "chatId": self.chat_id,
            "type": t,
            "content": content
        }
        return await self.__send_packet("SETMETA", data)

    async def get_link_info(self):
        return await self.__send_packet("INFOLINK", {"lis": [self.li]})

    async def get_chat_info(self):
        return await self.__send_packet("CHATINFO", {"chatId": self.chat_id})

    async def get_user_info(self, user_id):
        return await self.__send_packet("MEMBER", {"chatId": self.chat_id, "memberIds": [user_id]})
