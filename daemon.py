
# Host ngrok server
# Send the ip to server to provide to other users
# Then host the socket server

import socket
import time
import random
import threading
import pickle
from pyngrok import ngrok

SV_IP	= "127.0.0.1"
SV_PORT = 5050
SV_ADDR = (SV_IP, SV_PORT)

CLIENT_IP = "127.0.0.1"
CLIENT_PORT = random.randint(1000, 9999) 
CLIENT_ADDR = (CLIENT_IP, CLIENT_PORT)

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

# User id
user_id = int(server.recv(BUFFER).decode(FORMAT))

# Starting a ngrok 
tcp_tunnel = ngrok.connect(CLIENT_PORT, "tcp")
url = tcp_tunnel.public_url
split = url.split(":")
host_url = split[1].split("//")[1]

# Getting ip and port
ip = socket.gethostbyname(host_url)
port = split[2]
cli_addr = {"ip": ip, "port": port}
server.send(pickle.dumps(cli_addr))

# Our hosted server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(CLIENT_ADDR)

# All the online users ip and port
online_users = []
peers_threads = []

# Packets
packets = []

# Parser
def packet_parser():
	print(packets)
	while True:
		for i in packets:
			if CLIENTS in i:
				clients = i[CLIENTS]
				online_users.clear()
				for j in clients:
					online_users.append(clients[j])
				packets.remove(i)

# Listeners
def server_listener():
	while True:
		data = server.recv(BUFFER)
		if data:
			packets.append(pickle.loads(data))

def peer_listener(idx):
	addr = online_users[idx]
	peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	peer.connect((addr["ip"], addr["port"]))

	while True:
		data = peer.recv(BUFFER)
		if data:
			packets.append(pickle.loads(data))
		else:
			break

def peer_send(packet):
	if len(online_users) > 1:
		addr = random.choice(online_users)	
		if addr["port"] != CLIENT_PORT:
			peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			peer.connect((addr["ip"], addr["port"]))
			print(addr, packet)
			peer.send(pickle.dumps(packet))
			peer.close()

def run_listeners():
	for idx in range(1, len(online_users)):
		thread = threading.Thread(target = peer_listener, args = (idx,))
		thread.start()
		peers_threads.append(thread)

if __name__ == "__main__":
	sv_listen_thread = threading.Thread(target = server_listener)
	sv_listen_thread.start()

	parser_thread = threading.Thread(target = packet_parser)
	parser_thread.start()

	run_listeners()
	packet = {"Helo": "World"}
	while True:
		peer_send(packet)
		#print(packets)
