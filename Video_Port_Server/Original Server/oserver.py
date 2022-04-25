# This code will run the drone side, it will send video to cache server


from concurrent.futures import ThreadPoolExecutor
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


host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)


def init_video(camera):
    # create server socket with tcp (one to many SOCK_STREAM standards )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    videoPort = 9999
    socket_address = (host_ip, videoPort)
    server_socket.bind(socket_address)
    server_socket.listen()
    print("Listening at video port", socket_address)
    client_socket, addr = server_socket.accept()
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture('piano.mp4')
    try:
        print('Cached Server {} Connected !'.format(addr))
        if client_socket:
            while(vid.isOpened()):
                img, frame = vid.read()

                frame = imutils.resize(frame, width=600)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)
                cv2.imshow("Transfering to bufferd Server", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    break

    except Exception as e:
        print(f"Cached Server  {addr} Disconnected")
        pass


def main():
    val = int(input("Choose: \nLive stream: 1 \nLive video:2 \n"))
    if(val == 1):
        with ThreadPoolExecutor(max_workers=1) as executorStream:
            executorStream.submit(init_video, True)
    else:
        with ThreadPoolExecutor(max_workers=1) as executorVideo:
            executorVideo.submit(init_video, False)


if __name__ == "__main__":
    main()
