import asyncio


class Writer:
    def __init__(self, crypto, stream_writer, packet_dict):
        self.crypto = crypto
        self.stream_writer = stream_writer
        self.packet_id = 0
        self.packet_dict = packet_dict

    def __get_packet_id(self):
        self.packet_id += 1
        return self.packet_id

    async def send_packet(self, packet):
        pid = self.__get_packet_id()

        fut = asyncio.get_event_loop().create_future()
        self.packet_dict[pid] = fut

        packet.packet_id = pid
        self.stream_writer.write(packet.to_encrypted_loco_packet(self.crypto))
        await self.stream_writer.drain()

        return await fut
