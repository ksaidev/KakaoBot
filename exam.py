import client
from packet import Packet
import bson
import time
import json

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


client = MyClass("DEVICE NAME")
client.run("id", "pw")
