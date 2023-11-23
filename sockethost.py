import socket

IP = '127.0.0.1'
PORT = 8005
BUFLEN = 512

listenSocket = socket.socket()

listenSocket.bind((IP, PORT))

listenSocket.listen(5)
print ("init well, wait for connect")

dataSocket, addr = listenSocket.accept()
print ("cheaked", addr)

while True:
    s  = input("here")
    dataSocket.send(s.encode())


dataSocket.close()
listenSocket.close()
    



