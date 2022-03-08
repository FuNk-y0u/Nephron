# TODO: Make the data pass through server to the other clients
# or Make server as a bridget between users

import socket
import pickle
import threading
import random
import time

IP	 = "127.0.0.1"
PORT = 5050
BUFFER = 1024
FORMAT = "utf-8"

# TOKENS
DATA = "data"
PACKET = "packet"
PUSH = "push"
PULL = "pull"
CLIENTS = "clients"
PACKETID = "packetid"
class Packet:
	def __init__(self, id, offset, data):
		self.id = id
		self.offset = offset 
		self.data = data.encode(FORMAT)

class Server:
	def __init__(self):
		self.__create_server()
		self.running = True
		self.online_cons  = []
		self.packets = []
		self.data_tracker = {}
	
	def __create_server(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((IP, PORT))
	
	def __remove_client(self, conn):
		self.online_cons.remove(conn)
	
	def __packet_handler(self):
		while True:
			#print(self.packets)
			packets = self.packets.copy()
			for packet in packets:
				conn = random.choice(self.online_cons)
				conn.send(pickle.dumps(packet))
				self.packets.remove(packet)

	def __handle_client(self, conn, addr):
		while True:
			print("test 2")
			try:
				print("test 3")
				data = conn.recv(BUFFER)
				print(data)
				print("test 4")
				if not data:
					self.__remove_cons(conn)
					break
			
				packet = pickle.loads(data)
				self.packets.append(packet)
				time.sleep("0.5")
			except ConnectionResetError:
				print("test 4")
				self.__remove_cons(conn)
				break
			#datachunks = pickle.loads(b""+join(datachunks))
			#print(datachunks)
		conn.close()
	
	def run(self):
		self.server.listen()
		print(f"Server listening in {IP}")
		
		while self.running:
			conn, addr = self.server.accept()

			# Addding the new user to group
			self.online_cons.append(conn)

			cli_handler_thread = threading.Thread(target=self.__handle_client, args=(conn, addr))
			cli_handler_thread.start()

			packet_handler_thread = threading.Thread(target=self.__packet_handler)
			packet_handler_thread.start()

if __name__ == "__main__":
	server = Server()
	server.run()
