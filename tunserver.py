import socket
import sys
import time
import threading
import base64

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.setblocking(0)

stop_flag = False

def back_worker():
    global stop_flag
    while not stop_flag:
        r = raw_input().strip()
        if r == '!':
            stop_flag = True
        else:
            s.sendall(base64.b64decode(r))

back_thread = threading.Thread(target = back_worker)
back_thread.start()

while not stop_flag:
    time.sleep(0.1)
    try:
        r = s.recv(1024)
    except socket.error:
        r = ''
    if len(r) > 0:
        print base64.b64encode(r)

