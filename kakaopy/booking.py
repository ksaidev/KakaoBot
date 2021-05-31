import socket
import ssl

from .packet import Packet

import bson


def get_booking_data():
    hostname = 'booking-loco.kakao.com'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            data = bson.BSON.encode({'os': "win32", "model": "", "MCCMNC": ""})

            b = Packet(1000, 0, "GETCONF", 0, data)
            ssock.write(b.to_loco_packet())

            data = ssock.recv(4096)

            recvPacket = Packet()
            recvPacket.read_loco_packet(data)
            return recvPacket
