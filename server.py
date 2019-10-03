import socket
from threading import Thread
import os

HOST = '0.0.0.0'
PORT = 59999
BUFFER_SIZE = 1024


class ClientListener(Thread):
    def __init__(self, sock):
        super().__init__(daemon=True)
        self.sock = sock

    def run(self):
        filename = None
        if not os.path.isdir('files'):
            os.mkdir('files')
        print(f'\nConnected at {addr}', end="\n")
        i = 0
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            if i == 0:
                filename = data.decode('utf-8')
                print("Receiving", filename)
                if filename in os.listdir('files'):
                    same_filenames_list = [file for file in os.listdir('files') if
                                           filename.split('.')[0] + '_copy' in file]
                    filename_parts = filename.split('.')
                    if len(same_filenames_list) != 0:
                        print("File collisions:", same_filenames_list)
                        num = len(same_filenames_list) + 1
                        filename = filename_parts[0] + f'_copy{str(num)}.' + filename_parts[1]
                    else:
                        filename = filename_parts[0] + '_copy1.' + filename_parts[1]
                f = open(f'files/{filename}', 'wb')
                i += 1
                conn.sendall(b'ok')
            else:
                f.write(data)
        f.close()
        if filename:
            print(f"Received {filename}")


print("Server is on. Waiting for incoming connections...")
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        ClientListener(conn).start()
