import socket
import time

IP = '127.0.0.1'
PORT = 8005
BUFLEN = 512

dataSocket = socket.socket()

dataSocket.connect((IP, PORT))

while True:
    toSend = input (">>")
    if toSend == "":
        break
    dataSocket.send(toSend.encode())
    received = dataSocket.recv(BUFLEN)
    if not received:
        break
    print (received.decode())

dataSocket.close()


