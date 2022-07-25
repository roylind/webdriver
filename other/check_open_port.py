import socket
import random


def search_close_port():
	for _ in range(10):
		temp_port = random.randrange(3000, 10000, 1)
		if (check_port(temp_port) == False):
			return(temp_port)
	raise Exception("Not Found Close Port")


def check_port(port):
	# Create a TCP socket
	address = "localhost"
	s = socket.socket()
	# print("Attempting to connect to %s on port %s" % (address, port))
	try:
		s.connect((address, port))
		# print("Connected to %s on port %s" % (address, port))
		return True
	except socket.error as e:
		# print("Connection to %s on port %s failed: %s" % (address, port, e))
		return False
	finally:
		s.close()