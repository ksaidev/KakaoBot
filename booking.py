import socket
import ssl
import packet
import bson

def getBookingData():
    hostname = 'booking-loco.kakao.com'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            data = bson.BSON.encode(
                {'os': "win32", "model": "", "MCCMNC": ""})

            b = packet.Packet(1000, 0, "GETCONF", 0, data)
            ssock.write(b.toLocoPacket())

            data = ssock.recv(4096)
            
            recvPacket = packet.Packet()
            recvPacket.readLocoPacket(data)
            return recvPacket

