from socket import socket

from .crypto_manager import CryptoManager
from .packet import Packet

import bson


def get_check_in_data(host: str, port: int):
    crypto = CryptoManager()

    sock = socket()
    sock.connect((host, port))

    handshake_packet = crypto.get_handshake_packet()
    sock.send(handshake_packet)

    p = Packet(1, 0, "CHECKIN", 0, bson.encode({
        "userId": 0,
        "os": "win32",
        "ntype": 0,
        "appVer": "3.14",
        "MCCMNC": "999",
        "lang": "ko",
    }))

    sock.send(p.to_encrypted_loco_packet(crypto))

    data = sock.recv(2048)

    recv_packet = Packet()
    recv_packet.read_encrypted_loco_packet(data, crypto)

    return recv_packet
