import socket
import select
import sys
 

if(len(sys.argv) <3) :
	print 'Format : python client.py hostname port'
	sys.exit()
 
host = sys.argv[1]
port = int(sys.argv[2])
 
socketclient = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
 
# Connection establishment with the server
try : socketclient.connect((host, port))
except :
	print 'Unable to connect'
	sys.exit()
 
print "You have joined the chat room! Start messaging to know others!\n"
print "Type 'disconnect' to leave chatroom"
sys.stdout.write('Me: ')
sys.stdout.flush()
 
while True:
	messagesocket = [sys.stdin, socketclient]
	 
	# Getting readable sockets and reading them with select
	readsock, writesock, errsock = select.select(messagesocket , [], [])
	 
	for sock in readsock:
		#Message received from server
		if sock is not socketclient:
			#when client wants to send a message
			msg = sys.stdin.readline()
			socketclient.send(msg)
			sys.stdout.write('Me: ')
			sys.stdout.flush()

		else :	
			#data recevied from the RECV_BUFFER in the server
			data = sock.recv(4096)
			if not data :
				#if client is disconnected from the server
				print '\nDisconnected from chat server'
				sys.exit()
			else :
				#receive message from other clients
				sys.stdout.write(data)
				sys.stdout.write('Me: ')
				sys.stdout.flush()
