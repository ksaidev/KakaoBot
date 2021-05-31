from kakaopy.client import Client
import json

class CustomClient(Client):
    async def onPacket(self, packet):
        name = packet.PacketName
        body = packet.toJsonBody()
        # print(f"{name} | {body}")

    async def onMessage(self, chat):
        print(chat.message)

        if chat.message == "TEST":
            await chat.reply("KAKAOPY is running")

        if chat.message == "태그":
            # 이와 같은 방식으로 메세지를 보내는 법은 깃헙 위키에 나와 있습니다
            attachment = {'mentions': [{'user_id': chat.authorId, 'at': [1], 'len': 2}]}
            await chat.channel.sendChat("@태그", json.dumps(attachment), 1)
            
        # 자신의 메시지의 경우
        if chat.message == ".삭제":
            await chat.delete()

        # OpenChat 권한 있는 경우
        if chat.message == ".가리기":
            await chat.hide()
