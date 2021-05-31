from .booking import get_booking_data
from .check_in import get_check_in_data
from .crypto_manager import CryptoManager
from .http_api import post_text, login
from .writer import Writer
from .chat import Chat
from .channel import Channel
from .packet import Packet


import json
import asyncio
import struct
from socket import socket
import bson


class Client:
    def __init__(self, device_name, device_uuid):
        self.__sock: socket
        self.__stream_reader: asyncio.StreamReader
        self.__stream_writer: asyncio.StreamWriter
        self.__crypto: CryptoManager
        self.__writer: Writer
        self.__access_key: str

        self.device_name = device_name
        self.device_uuid = device_uuid

        self.__packet_id = 0

        self.__processing_buffer = b""
        self.__processing_header = b""
        self.__processing_size = 0

        self.packetDict = {}
        self.loop = None

    def post_text(self, chat_id, li, text, notice=False):
        post_text(chat_id, li, text, notice,
                  self.__access_key, self.device_uuid)

    async def __recv_packet(self):
        encrypted_buffer = b""
        current_packet_size = 0

        while True:
            recv = await self.__stream_reader.read(256)

            if not recv:
                print(recv)
                self.loop.stop()
                break

            encrypted_buffer += recv

            if not current_packet_size and len(encrypted_buffer) >= 4:
                current_packet_size = struct.unpack(
                    "<I", encrypted_buffer[0:4])[0]

            if current_packet_size:
                encrypted_packet_size = current_packet_size+4

                if len(encrypted_buffer) >= encrypted_packet_size:
                    self.loop.create_task(self.__processing_packet(
                        encrypted_buffer[0:encrypted_packet_size]))
                    encrypted_buffer = encrypted_buffer[encrypted_packet_size:]
                    current_packet_size = 0

    async def __processing_packet(self, encrypted_packet):
        enc_len = encrypted_packet[0:4]
        iv = encrypted_packet[4:20]
        body = encrypted_packet[20:]

        self.__processing_buffer += self.__crypto.aes_decrypt(body, iv)

        if not self.__processing_header and len(self.__processing_buffer) >= 22:
            self.__processing_header = self.__processing_buffer[0:22]
            self.__processing_size = struct.unpack(
                "<i", self.__processing_header[18:22])[0] + 22

        if self.__processing_header:
            if len(self.__processing_buffer) >= self.__processing_size:
                p = Packet()
                p.read_loco_packet(
                    self.__processing_buffer[:self.__processing_size])

                self.loop.create_task(self.__on_packet(p))

                self.__processing_buffer = self.__processing_buffer[self.__processing_size:]
                self.__processing_header = b""

    async def __on_packet(self, packet):
        if packet.packet_id in self.packetDict:
            self.packetDict[packet.packet_id].set_result(packet)
            del self.packetDict[packet.packet_id]

        self.loop.create_task(self.on_packet(packet))

        body = packet.to_json_body()

        if packet.packet_name == "MSG":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            chat = Chat(channel, body)

            self.loop.create_task(self.on_message(chat))

        if packet.packet_name == "NEWMEM":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            self.loop.create_task(self.on_join(packet, channel))

        if packet.packet_name == "DELMEM":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            self.loop.create_task(self.on_quit(packet, channel))

        if packet.packet_name == "DECUNREAD":
            chatId = body["chatId"]

            channel = Channel(chatId, 0, self.__writer)
            self.loop.create_task(self.on_read(channel, body))

    async def on_packet(self, packet):
        pass

    async def on_message(self, chat):
        pass

    async def on_join(self, packet, channel):
        pass

    async def on_quit(self, packet, channel):
        pass

    async def on_read(self, channel, packet):
        pass

    async def __heartbeat(self):
        while True:
            await asyncio.sleep(180)
            PingPacket = Packet(0, 0, "PING", 0, bson.encode({}))
            self.loop.create_task(self.__writer.send_packet(PingPacket))

    async def __login(self, login_id, login_pw, ):
        r = json.loads(login(login_id, login_pw,
                             self.device_name, self.device_uuid))

        if r["status"] == -101:
            print("이전에 로그인이 되어있는 PC에서 로그아웃 해주세요")

        elif r["status"] == -100:
            print("디바이스 등록이 되어 있지 않습니다")

        elif r["status"] == 12:
            print("카카오계정 또는 비밀번호를 다시 확인해 주세요")

        if r["status"] != 0:
            self.loop.stop()
            raise Exception(str(r))

        self.__access_key = r["access_token"]
        # print(self.__accessKey)

        booking_data = get_booking_data().to_json_body()

        check_in_data = get_check_in_data(
            booking_data["ticket"]["lsl"][0],
            booking_data["wifi"]["ports"][0]).to_json_body()

        self.__stream_reader, self.__stream_writer = await asyncio.open_connection(
            check_in_data["host"], int(check_in_data["port"]))

        self.__crypto = CryptoManager()
        self.__writer = Writer(
            self.__crypto, self.__stream_writer, self.packetDict)

        LoginListPacket = Packet(0, 0, "LOGINLIST", 0, bson.encode({
            "appVer": "3.1.4",
            "prtVer": "1",
            "os": "win32",
            "lang": "ko",
            "duuid": self.device_uuid,
            "oauthToken": self.__access_key,
            "dtype": 1,
            "ntype": 0,
            "MCCMNC": "999",
            "revision": 0,
            "chatIds": [],
            "maxIds": [],
            "lastTokenId": 0,
            "lbk": 0,
            "bg": False,
        }))

        self.__stream_writer.write(self.__crypto.get_handshake_packet())

        self.loop.create_task(self.__writer.send_packet(LoginListPacket))

        self.loop.create_task(self.__recv_packet())
        self.loop.create_task(self.__heartbeat())

    def run(self, login_id, login_pw):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__login(login_id, login_pw))
        self.loop.run_forever()
