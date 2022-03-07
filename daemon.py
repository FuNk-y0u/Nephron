import socket
import time
import random
import threading
import pickle
import os
from pyngrok import ngrok

SV_IP	= "127.0.0.1"
SV_PORT = 5050
SV_ADDR = (SV_IP, SV_PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(SV_ADDR)

BUFFER = 1024
PACKET_SIZE = 46080
FORMAT = "utf-8"

# TOKENS
DATA = "data"
PACKET = "packet"
PUSH = "push"
PULL = "pull"
CLIENTS = "clients"

class Packet:
	def __init__(self, id, offset, data):
		self.id = id
		self.offset = offset 
		self.data = data.encode(FORMAT)

# Packets
packets = []
# Listeners
def server_listener():
	while True:
		data = server.recv(BUFFER)
		if data:
			packets.append(pickle.loads(data))

# Packet sender
def send_packet(packet):
	packets.append(packet)

def packet_cleaner():
	# Sends all the packets in the packet list to the server
	global packets 
	while True:
		pack_copy = packets.copy()
		for packet in pack_copy:
			server.send(pickle.dumps(packet))
			packets.remove(packet)

# File handling
def chop_file(file):
	padding = PACKET_SIZE - (len(file) % PACKET_SIZE)
	file += b" " * padding
	packet_size = int(len(file) / PACKET_SIZE)

	chunk = []
	for i in range(0, len(file), PACKET_SIZE):
		chunk.append(file[i:i+PACKET_SIZE])
	
	return chunk

def send_file(file):
	if not os.path.exists(file):
		print(f"[ERROR]: {file} doesnt exists.")
		exit()
	
	# Reading the file
	with open(file, "rb") as f:
		file_data = f.read()

	# Choping the file into chunks
	chunk = chop_file(file_data)	
	
	#TODO: Create packets from the chunk and send to server
	print(chunk)

if __name__ == "__main__":
	sv_listen_thread = threading.Thread(target = server_listener)
	sv_listen_thread.start()

	packet_cleaner_thread = threading.Thread(target = packet_cleaner)
	packet_cleaner_thread.start()

	send_file("sample.txt")
	while True:
		pass

