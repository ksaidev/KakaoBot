import time
import json

from kakaopy.client import Client
from kakaopy.httpApi import RequestPasscode, RegisterDevice

import bson


class MyClass(Client):
    async def onPacket(self, packet):
        name = packet.PacketName
        body = packet.toJsonBody()
        # print(f"{name} | {body}")

    async def onMessage(self, chat):
        print(chat.message)

        if chat.message == "TEST":
            await chat.reply("KAKAOPY is running")

        # 자신의 메시지의 경우
        if chat.message == ".삭제":
            await chat.delete()

        # OpenChat 권한 있는 경우
        if chat.message == ".가리기":
            await chat.hide()


if __name__ == "__main__":
    user_id = str(input("ID : "))
    user_pw = str(input("PW : "))
    device_name = "KAKAOPY TEST"

    user_uuid = "REVWSUNFMQ=="  # TODO what's the meaning?
    RequestPasscode(user_id, user_pw, device_name, user_uuid)

    print("Please check your phone or computer for the authorization passcode")
    passcode = str(input("PASSCODE : "))
    RegisterDevice(user_id, user_pw, device_name, user_uuid, passcode)

    client = MyClass(device_name)
    client.run(user_id, user_pw)
