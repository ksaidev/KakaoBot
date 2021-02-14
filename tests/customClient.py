from kakaopy.client import Client


class CustomClient(Client):
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
