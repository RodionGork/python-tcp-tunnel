import base64
import socket
import subprocess
import sys
import time
import threading

stop_flag = False

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(('127.0.0.1', 5080))
srv.listen(60)
cli, addr = srv.accept()
cli.setblocking(0)

ssh = subprocess.Popen(['ssh', '-t', '-t', sys.argv[1], 'stty -echo;' + sys.argv[2]], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

recvd = 0
recvd_reported = 1000

def back_worker():
    global stop_flag, recvd, recvd_reported
    while not stop_flag:
        try:
            r = cli.recv(1024)
        except socket.error:
            continue
        ssh.stdin.write(base64.b64encode(r) + '\r\n')
        recvd += len(r)
        if recvd > recvd_reported:
            print 'Out: %s' % recvd
            recvd_reported += 1000

back_thread = threading.Thread(target = back_worker)
back_thread.start()

sent = 0
sent_reported = 1000

while not stop_flag:
    r = ssh.stdout.readline()
    cli.sendall(base64.b64decode(r))
    sent += len(r)
    if sent > sent_reported:
        print 'In: %s' % sent
        sent_reported += 1000

