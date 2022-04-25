
import socket
import cv2
import pickle
import struct
import imutils  # pip install imutils
import threading
import cv2
import socket
import os
import threading
import wave
import pyaudio
import pyshine as ps
from concurrent.futures import ThreadPoolExecutor

# create client socket and get data from cached server


def audio_stream():
    name = 'Client Receiving Audio'
    audio, context = ps.audioCapture(mode='get')
    # ps.showPlot(context, name)

    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_ip = '192.168.0.112'
    host_ip = '127.0.0.1'
    port = 9998
    socket_address = (host_ip, port)
    client_socket.connect(socket_address)
    print("Client Connected To", socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        audio.put(frame)


def audio_video():
    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '127.0.0.1'  # Here Require CACHE Server IP
    port = 9998
    client_socket.connect((host_ip, port))  # a tuple
    print("Client connected to video server port", (host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        stream.write(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    client_socket.close()


def video():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '127.0.0.1'  # Here Require CACHE Server IP
    port = 9999
    client_socket.connect((host_ip, port))  # a tuple
    print("Client connected to video server port", (host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO ", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    client_socket.close()


def main():
    val = int(input("Choose: \nLive stream: 1 \nLive video:2 \n"))
    if(val == 1):
        with ThreadPoolExecutor(max_workers=2) as executorStream:
            executorStream.submit(audio_stream)
            executorStream.submit(video)
    else:
        with ThreadPoolExecutor(max_workers=2) as executorVideo:
            executorVideo.submit(audio_video)
            executorVideo.submit(video)


#  main
if __name__ == "__main__":
    main()
