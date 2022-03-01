import socket
import threading

IP	 = "127.0.0.1"
PORT = 5050

class Server:
	def __init__(self):
		self.__create_server()
		self.running = True
		self.online_users = []	# TODO: Maybe change to dictionary when usernames are indroduced
	
	def __create_server(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((IP, PORT))

	def __handle_client(self, conn):
		while True:
			on_user = " ".join(f"{i}" for i in self.online_users)
			try:
				conn.send(on_user)
			except socket.error:
				self.online_users.remove(conn)
				break
		conn.close()
	
	def run(self):
		self.server.listen()
		print(f"Server listening in {self.ip}")
		
		while self.running:
			conn, addr = self.server.accept()
			# Addding the new user to group
			self.online_users.append(conn);

			new_thread = threading.Thread(target=self.__handle_client, args=(conn, ))
			new_thread.start()

if __name__ == "__main__":
		
