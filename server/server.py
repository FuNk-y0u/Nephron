import socket
import pickle
import threading
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

class Server:
	def __init__(self):
		self.__create_server()
		self.running = True
		self.user_offset = 0
		self.online_cons  = []
		self.online_users = {CLIENTS: {}} # TODO: Maybe change to dictionary when usernames are indroduced
	
	def __create_server(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((IP, PORT))

	def __handle_client(self, user_offset, conn, addr):
		while True:
			time.sleep(0.5)
			try:
				data = conn.recv(BUFFER)
				if not data:
					self.online_users[CLIENTS].pop(user_offset)
					self.online_cons.remove(conn)
					for i in self.online_cons:
						i.send(pickle.dumps(self.online_users))
					break
			except ConnectionResetError:
				self.online_users[CLIENTS].pop(user_offset)
				self.online_cons.remove(conn)
				for i in self.online_cons:
					i.send(pickle.dumps(self.online_users))
				break

		conn.close()
	
	def run(self):
		self.server.listen()
		print(f"Server listening in {IP}")
		
		while self.running:
			conn, addr = self.server.accept()

			# Addding the new user to group
			self.online_cons.append(conn)

			conn.send(f"{self.user_offset}".encode(FORMAT))
			client_addr = pickle.loads(conn.recv(BUFFER))

			self.online_users[CLIENTS].update({self.user_offset: client_addr})
			for i in self.online_cons:
				i.send(pickle.dumps(self.online_users))

			print(self.online_users)

			new_thread = threading.Thread(target=self.__handle_client, args=(self.user_offset, conn, addr))
			new_thread.start()
			self.user_offset += 1

if __name__ == "__main__":
	server = Server()
	server.run()
