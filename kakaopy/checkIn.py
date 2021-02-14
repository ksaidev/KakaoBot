from socket import socket
import io
import struct

from .cryptoManager import CryptoManager
from .packet import Packet

from bson import BSON as bson


def getCheckInData(host: str, port: int):
    crypto = CryptoManager()

    sock = socket()
    sock.connect((host, port))

    handshakePacket = crypto.getHandshakePacket()
    sock.send(handshakePacket)

    p = Packet(1, 0, "CHECKIN", 0, bson.encode({
        "userId": 0,
        "os": "win32",
        "ntype": 0,
        "appVer": "3.14",
        "MCCMNC": "999",
        "lang": "ko",
    }))

    sock.send(p.toEncryptedLocoPacket(crypto))

    data = sock.recv(2048)

    recvPacket = Packet()
    recvPacket.readEncryptedLocoPacket(data, crypto)

    return recvPacket
