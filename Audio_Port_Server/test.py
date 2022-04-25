import socket
import cv2
import pickle
import struct
import time
import pyshine as ps #pip3 install pyshine==0.0.6


name = 'SERVER TRANSMITTING AUDIO'
audio, context = ps.audioCapture(mode='send')
ps.showPlot(context, name)

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.112'
port = 4982
backlog = 5
socket_address = (host_ip, port)
print('STARTING SERVER AT', socket_address, '...')
server_socket.bind(socket_address)
server_socket.listen(backlog)

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:

        while(True):
            frame = audio.get()

            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)

    else:
        break

client_socket.close()
