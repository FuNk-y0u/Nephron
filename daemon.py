import socket
import time
import random
import threading
import pickle
from pyngrok import ngrok

SV_IP	= "127.0.0.1"
SV_PORT = 5050
SV_ADDR = (SV_IP, SV_PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(SV_ADDR)

BUFFER = 1024
FORMAT = "utf-8"

# TOKENS
DATA = "data"
PACKET = "packet"
PUSH = "push"
PULL = "pull"
CLIENTS = "clients"

# Packets
packets = []
# Listeners
def server_listener():
	while True:
		data = server.recv(BUFFER)
		if data:
			packets.append(pickle.loads(data))

# Packet sender
def server_send(packet):
	packets.append(packet)

def packet_cleaner():
	# Sends all the packets in the packet list to the server
	global packets 
	while True:
		pack_copy = packets.copy()
		for packet in pack_copy:
			server.send(pickle.dumps(packet))
			packets.remove(packet)

if __name__ == "__main__":
	sv_listen_thread = threading.Thread(target = server_listener)
	sv_listen_thread.start()

	packet_cleaner_thread = threading.Thread(target = packet_cleaner)
	packet_cleaner_thread.start()

	packet = {PACKET: "Hello World"}
	server_send(packet)	
	while True:
		pass

