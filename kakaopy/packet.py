import os
import io
import struct

import bson


class Packet:
    def __init__(self, packet_id=0, status_code=0, packet_name="", body_type=0, body=b""):
        self.packet_id = packet_id
        self.status_code = status_code
        self.packet_name = packet_name
        self.body_type = body_type
        self.body_size = 0
        self.body = body

    def to_loco_packet(self):
        f = io.BytesIO()
        f.write(struct.pack("<I", self.packet_id))
        f.write(struct.pack("<H", self.status_code))

        if (11-len(self.packet_name)) < 0:
            raise Exception("invalid packetName")

        f.write(self.packet_name.encode("utf-8"))

        f.write(b"\x00" * (11 - len(self.packet_name)))
        f.write(struct.pack("<b", self.body_type))
        f.write(struct.pack("<i", len(self.body)))

        f.write(self.body)
        return f.getvalue()

    def read_loco_packet(self, packet):
        self.packet_id = struct.unpack("<I", packet[:4])[0]
        self.status_code = struct.unpack("<H", packet[4:6])[0]
        self.packet_name = packet[6:17].decode().replace("\0", "")
        self.body_type = struct.unpack("<b", packet[17:18])[0]
        self.body_size = struct.unpack("<i", packet[18:22])[0]
        self.body = packet[22:]

    def to_encrypted_loco_packet(self, crypto):
        iv = os.urandom(16)
        encrypted_packet = crypto.aes_encrypt(self.to_loco_packet(), iv)

        f = io.BytesIO()
        f.write(struct.pack("<I", len(encrypted_packet)+len(iv)))
        f.write(iv)
        f.write(encrypted_packet)

        return f.getvalue()

    def read_encrypted_loco_packet(self, packet, crypto):
        packetLen = struct.unpack(">I", packet[0:4])[0]
        iv = packet[4:20]
        data = packet[20:packetLen-16]

        dec = crypto.aes_decrypt(data, iv)

        try:
            self.read_loco_packet(dec)
        except Exception as e:
            print(str(e))

    def to_json_body(self):
        return bson.decode(self.body)
