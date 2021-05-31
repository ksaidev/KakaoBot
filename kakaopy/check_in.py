from socket import socket

from .crypto_manager import CryptoManager
from .packet import Packet
from .config import APP_VERSION, AGENT, NTYPE, MCCMNC

import bson


def get_check_in_data(host: str, port: int):
    crypto = CryptoManager()

    sock = socket()
    sock.connect((host, port))

    handshake_packet = crypto.get_handshake_packet()
    sock.send(handshake_packet)

    p = Packet(1, 0, "CHECKIN", 0, bson.encode({
        "userId": 0,
        "os": AGENT,
        "ntype": NTYPE,
        "appVer": APP_VERSION,
        "MCCMNC": MCCMNC,
        "lang": "ko",
    }))

    sock.send(p.to_encrypted_loco_packet(crypto))

    data = sock.recv(2048)

    recv_packet = Packet()
    recv_packet.read_encrypted_loco_packet(data, crypto)

    return recv_packet
