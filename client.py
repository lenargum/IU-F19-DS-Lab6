import socket
import sys
import os

filename = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with open(filename, 'rb') as f:
        filesize = os.path.getsize(filename)
        payload = f.read(BUFFER_SIZE)
        s.connect((HOST, PORT))
        s.send(bytes(filename, encoding='utf-8'))
        resp = s.recv(BUFFER_SIZE)
        if resp == b'ok':
            i = 1
            while payload:
                s.send(payload)
                upload_status = round(100 * (i * BUFFER_SIZE / filesize))
                if upload_status > 100:
                    upload_status = 100
                print(f"Transfer Progress: {upload_status}%", flush=True)
                i += 1
                payload = f.read(BUFFER_SIZE)
            f.close()
