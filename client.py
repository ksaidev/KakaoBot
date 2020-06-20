from socket import socket

import booking
import checkIn
import asyncio
import cryptoManager
import time
from packet import Packet
from bson import BSON as bson
import httpLogin
import json
import struct
class Client:
    def __init__(self, device_name="DEVICE", device_uuid = "REVWSUNFMQ=="):
        self.__sock: Socket
        self.__reader: asyncio.StreamReader
        self.__writer: asyncio.StreamWriter
        self.__crypto: cryptoManager.CryptoManager
        self.__accessKey: str

        self.device_name = device_name
        self.device_uuid = device_uuid

        
        self.__packetID = 0

        self.__processingBuffer = b""
        self.__processingHeader = b""
        self.__processingSize = 0

    async def __recvPacket(self):
        encryptedBuffer = b""
        currentPacketSize = 0

        while True:
            recv = await self.__reader.read(512)
            
            if not recv:
                print(recv)
                self.loop.stop()
            
            encryptedBuffer += recv

            if not currentPacketSize and len(encryptedBuffer) >= 4:
                currentPacketSize = struct.unpack(
                    "<I", encryptedBuffer[0:4])[0]

            if currentPacketSize:
                encryptedPacketSize = currentPacketSize+4

                if len(encryptedBuffer) >= encryptedPacketSize:
                    self.loop.create_task(self.__processingPacket(encryptedBuffer[0:encryptedPacketSize]))
                    encryptedBuffer = encryptedBuffer[encryptedPacketSize:]
                    currentPacketSize = 0

    async def __processingPacket(self, encryptedPacket):
        encLen = encryptedPacket[0:4]
        IV = encryptedPacket[4:20]
        BODY = encryptedPacket[20:]
        
        self.__processingBuffer += self.__crypto.aesDecrypt(BODY, IV)

        if not self.__processingHeader and len(self.__processingBuffer) >= 22:
            self.__processingHeader = self.__processingBuffer[0:22]
            self.__processingSize = struct.unpack(
                "<i", self.__processingHeader[18:22])[0] + 22

        if self.__processingHeader:
            if len(self.__processingBuffer) >= self.__processingSize:
                p = Packet()
                p.readLocoPacket(self.__processingBuffer[:self.__processingSize])
                
                self.loop.create_task(self.onPacket(p))
                self.__processingBuffer = self.__processingBuffer[self.__processingSize:]
                self.__processingHeader = b""

    async def onPacket(self, packet):
        #stub
        pass
    
    async def __heartbeat(self):
        while True:
            await asyncio.sleep(180)
            PingPacket = Packet(self.__getPacketID(), 0, "PING", 0, bson.encode({}))
            self.__writer.write(
                PingPacket.toEncryptedLocoPacket(self.__crypto))
            await self.__writer.drain()

    def __getPacketID(self):
        self.__packetID += 1
        return self.__packetID

    def run(self, LoginId, LoginPw):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__login(LoginId, LoginPw))
        self.loop.run_forever()

    async def __login(self, LoginId, LoginPw,):
        r = httpLogin.Login(LoginId, LoginPw, self.device_name, self.device_uuid)

        self.__accessKey = json.loads(r)["access_token"]
        #print(self.__accessKey)
        
        bookingData = booking.getBookingData().toJsonBody()

        checkInData = checkIn.getCheckInData(
            bookingData["ticket"]["lsl"][0],
            bookingData["wifi"]["ports"][0]).toJsonBody()

        self.__reader, self.__writer = await asyncio.open_connection(checkInData["host"], int(checkInData["port"]))

        self.__crypto = cryptoManager.CryptoManager()
        
        LoginListPacket = Packet(self.__getPacketID(), 0, "LOGINLIST", 0, bson.encode({
            "appVer": "3.1.1.2441",
            "prtVer": "1",
            "os": "win32",
            "lang": "ko",
            "duuid": self.device_uuid,
            "oauthToken": self.__accessKey,
            "dtype": 1,
            "ntype": 0,
            "MCCMNC": "",
            "revision": 0,
            "chatIds": [],
            "maxIds": [],
            "lastTokenId": 0,
            "lbk": 0,
            "bg": False,
        }))

        self.__writer.write(self.__crypto.getHandshakePacket())

        self.__writer.write(
            LoginListPacket.toEncryptedLocoPacket(self.__crypto))
        await self.__writer.drain()

        self.loop.create_task(self.__recvPacket())
        self.loop.create_task(self.__heartbeat())
        
