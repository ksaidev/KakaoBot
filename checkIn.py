from socket import socket
import cryptoManager
import packet
import io
from bson import BSON as bson
import struct

def getCheckInData(host :str, port :int):
	crypto=cryptoManager.CryptoManager()
	
	sock=socket()
	sock.connect((host, port))

	handshakePacket = crypto.getHandshakePacket()
	sock.send(handshakePacket)
	
	p = packet.Packet(1, 0, "CHECKIN", 0, bson.encode({
	    "userId": 0,
	    "os": "android",
	    "ntype": 0,
	    "appVer": "8.8.6",
	    "MCCMNC": "45005",
	    "lang": "ko",
	}))

	sock.send(p.toEncryptedLocoPacket(crypto))

	data=sock.recv(2048)

	recvPacket = packet.Packet()
	recvPacket.readEncryptedLocoPacket(data, crypto)
	
	return recvPacket
	
