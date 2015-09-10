# Chat server where multiple clients can connect to the server.
#The server reads the message sent by each lient and broadcasts it to all other connected clients.

import socket
import select
 
#list of socket descriptors (readable client connections)
#Socket descriptors are like file descriptors, in this case used for reading some text which the client sends
SOCKET_DESC = []

#Buffer in which messages received from clients are stored
RECV_BUFFER = 4096

#port on which chat server will listening
PORT = 5000

#creating an INET Stream socket.
#Stream sockets transmit data reliably, in order and woth out of band capabilities.
serversocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# Binds the socket to a host and a port and then listens for incoming connections
serversocket.bind(("::", PORT))
serversocket.listen(10)

# Add server socket to list of socket descriptors
SOCKET_DESC.append(serversocket)

print "Chat server running on port " + str(PORT)

# function for broadcasting a client's message to all other clients connected to the server
def clientbroadcast (sock, message):
	for socket in SOCKET_DESC:
		#if the socket is not the client's socket itself or it is not the server's socket, message will be broadcast
		if socket is not sock and socket is not serversocket:
			try : socket.send(message)
			except :
				socket.close()
				SOCKET_DESC.remove(socket)

while True:
	# Gets list of readable sockets. These are read using select
	readsock, writesock, errsock = select.select(SOCKET_DESC, [], [])

	# case in which a new connection is handled
	for sock in readsock:
		if sock is serversocket:
			# New connection received though serversocket, i.e., a new client has connected to the server.
			# The connection is accepted using the .accept() method. It returns (connfd, addr) where connfd is a
			# new socket object used to send/receive data on the connection and sddr is the address bound to the 
			# socket on the other end of the connection
			connfd, addr = serversocket.accept()

			# The new client connection is added to the list of connections
			SOCKET_DESC.append(connfd)

			print "Client " + str(addr) +" connected"

			#clientbroadcast function called
			clientbroadcast(connfd, str(addr) + " entered chat room" + "\n")
		 
		# case in which some client sends an incoming message
		else:
			try:
				# gets the data stored in the buffer
				clientdata = sock.recv(RECV_BUFFER)

				#if some data exists, it means that the client has sent a message
				# This message is broadcast to others connected to the server
				if clientdata:
					clientbroadcast(sock, "\r" + str(sock.getpeername()) + ': ' + clientdata)               
				
				#when client sends disconnect message
				if clientdata.split("\n")[0] == "disconnect":
					clientbroadcast(sock, "Client " + str(addr) + " left chat room!\n")
					print "Client " + str(addr) + " disconnected"
					sock.close()
					SOCKET_DESC.remove(sock)
					continue
			except:
				continue
	
serversocket.close()