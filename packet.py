from bson import BSON as bson
import cryptoManager
import os
import io
import struct


class Packet:
    def __init__(self, PacketID=0, StatusCode=0, PacketName="", BodyType=0, Body=b""):
        self.PacketID = PacketID
        self.StatusCode = StatusCode
        self.PacketName = PacketName
        self.BodyType = BodyType
        self.Body = Body

    def toLocoPacket(self):
        f = io.BytesIO()
        f.write(struct.pack("<I", self.PacketID))
        f.write(struct.pack("<H", self.StatusCode))

        if (11-len(self.PacketName)) < 0:
            raise Exception("invalid packetName")

        f.write(self.PacketName.encode("utf-8"))

        f.write(b"\x00"*(11-len(self.PacketName)))
        f.write(struct.pack("<b", self.BodyType))
        f.write(struct.pack("<i", len(self.Body)))

        f.write(self.Body)
        return f.getvalue()

    def readLocoPacket(self, packet):
        self.PacketID = struct.unpack("<I", packet[:4])[0]
        self.StatusCode = struct.unpack("<H", packet[4:6])[0]
        self.PacketName = packet[6:17].decode().replace("\0", "")
        self.BodyType = struct.unpack("<b", packet[17:18])[0]
        self.BodySize = struct.unpack("<i", packet[18:22])[0]
        self.Body = packet[22:]

    def toEncryptedLocoPacket(self, crypto):
        iv = os.urandom(16)
        encrypted_packet = crypto.aesEncrypt(self.toLocoPacket(), iv)

        f = io.BytesIO()
        f.write(struct.pack("<I", len(encrypted_packet)+len(iv)))
        f.write(iv)
        f.write(encrypted_packet)

        return f.getvalue()

    def readEncryptedLocoPacket(self, packet, crypto):
        packetLen = struct.unpack(">I", packet[0:4])[0]
        iv = packet[4:20]
        data = packet[20:packetLen-16]

        dec = crypto.aesDecrypt(data, iv)

        try:
            self.readLocoPacket(dec)
        except Exception as e:
            print(str(e))

    def toJsonBody(self):
        return bson.decode(self.Body)
