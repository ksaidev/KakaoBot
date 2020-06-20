import client


class MyClass(client.Client):
    async def onPacket(self, packet):
        print(packet.toJsonBody())
        print("\n")


client = MyClass("DEVICE NAME")
client.run("id", "pw")