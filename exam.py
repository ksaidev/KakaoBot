import time
import json

import client

from packet import Packet
import bson


class MyClass(client.Client):
    """
    async def onPacket(self, packet):
        name = packet.PacketName
        body = packet.toJsonBody()
        # print(name)
        print(body)
        # print("\n")
    """

    async def onMessage(self, chat):
        print(chat.message)

        if chat.message == "와":
            await chat.reply("샌주")
        
        #자신 메시지만
        if chat.message == ".삭제":
            await chat.delete()
        
        #OpenChat 권한 있을떄
        if chat.message == ".가리기":
            await chat.hide()

client = MyClass("DEVICE NAME")
client.run("id", "pw")
