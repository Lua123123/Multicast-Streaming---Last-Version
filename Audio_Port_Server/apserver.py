# This code will run the drone side, it will send video to cache server


from concurrent.futures import ThreadPoolExecutor
from re import T
import socket
import cv2
import pickle
import struct
import imutils
import cv2
import socket
import threading
import wave
import pyaudio
import os
import time
import pyshine as ps  # pip3 install pyshine==0.0.6


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def videoConfig():
    # generate audio type from mp4
    filename = 'piano.mp4'
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(
        filename, 'temp.wav')
    os.system(command)


def audio_video(addr, client_socket):
    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    # client_socket, addr = server_socket.accept()
    try:
        data = None
        while True:
            if client_socket:
                while True:

                    data = wf.readframes(CHUNK)
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a))+a
                    client_socket.sendall(message)
    except Exception as e:
        print(f"Client {addr} disconnected from Server audio port")
        pass


def audio_stream(addr, client_socket):
    name = 'Server Transmistting Audio'
    audio, context = ps.audioCapture(mode='send')
    # ps.showPlot(context, name)
    try:

        # client_socket, addr = server_socket.accept()
        print('Got Connection From:', addr)
        if client_socket:
            while(True):
                frame = audio.get()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)
    except Exception as e:
        print(f"Client {addr} disconnected from Server audio port")
        pass

    client_socket.close()


def main():
    val = int(input("Choose: \nAudio stream: 1 \nAudio from video:2 \n"))
    if(val == 1):
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name)
        host_ip = '127.0.0.1'
        serverPort = 9998
        socket_address = (host_ip, serverPort)
        print('STARTING SERVER AT', socket_address, '...')
        server_socket.bind(socket_address)
        server_socket.listen()
        # listen if having any new client
        while True:
            client_socket, addr = server_socket.accept()
            print(addr)
            # thread1 = threading.Thread(
            #     target=audio_stream, args=(addr, client_socket))
            # thread1.start()
            with ThreadPoolExecutor(max_workers=1) as executorAudioVideo:
                executorAudioVideo.submit(audio_stream, addr, client_socket)
            print("Clients are joining ",
                  threading.active_count() - 1)
    else:
        # config convert audio file from mp4
        # generate audio type from mp4
        videoConfig()
        # Socket Create
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '127.0.0.1'  # Enter the Drone IP address
        serverPort = 9998
        socket_address = (host_ip, serverPort)
        server_socket.bind((host_ip, serverPort))
        server_socket.listen()
        # listen if having any new client
        while True:
            client_socket, addr = server_socket.accept()
            print(addr)
            with ThreadPoolExecutor(max_workers=1) as executorAudioVideo:
                executorAudioVideo.submit(audio_video, addr, client_socket)
            # thread2 = threading.Thread(
            #     target=audio_video, args=(addr, client_socket))
            # thread2.start()
            print("Clients are joining ",
                  threading.active_count() - 1)


if __name__ == "__main__":
    main()
