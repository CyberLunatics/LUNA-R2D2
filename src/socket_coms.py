#!/usr/bin/python

import socket
import os, os.path
import threading
import time

PRINT_PREPEND = '[socket_coms.py] '

class UNIX_Coms():
    def __init__(self, host_addr):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server_address = host_addr

    def bind_to_socket(self):
        if os.path.exists(self.server_address):
            os.remove(self.server_address)
        self.sock.bind(self.server_address)
        print(PRINT_PREPEND + 'starting up on {}'.format(self.server_address))
        self.unix_start()

    def unix_start(self):
        threading.Thread(target=self.listen).start()

    def listen(self):
        print(PRINT_PREPEND + 'Listening for connections on {}'.format(self.server_address))
        while (True):
            data = self.sock.recv(4096)
            if data:
                os.system('capture-disk 5')
                os.system('echo capturing azure kinect images and saving to disk..')
                print(PRINT_PREPEND + 'Received data from {} | DATA [{}]: {}'.format(self.server_address, len(data), data))

    def connect_to_socket(self):
        connect = False
        try:
            print(PRINT_PREPEND + 'connecting to {}'.format(self.server_address))
            self.sock.connect(self.server_address)
            connect = True
            print(PRINT_PREPEND + 'Connected')
        except socket.error as msg:
            print(msg)

    def send(self, msg):
        print(PRINT_PREPEND + 'Sending data on socket: {}'.format(self.server_address))
        self.connect_to_socket()
        self.sock.sendall(msg)

    def close(self):
        self.sock.close()
        print(PRINT_PREPEND + 'Socket closed: {}'.format(self.server_address))

UNIX_SOCKETS_BASE_DIR = '/tmp/payload_sockets/'

UNIX_ADDR_OUT_1 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_3'
UNIX_ADDR_OUT_2 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_4'

UNIX_ADDR_IN_1 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_1'
UNIX_ADDR_IN_2 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_2'

def main():

    unix_in  = {}
    unix_out = {}

    try:
        unix_out = {
            'OUT_1' : UNIX_Coms(UNIX_ADDR_OUT_1),
            'OUT_2' : UNIX_Coms(UNIX_ADDR_OUT_2),
        }
    except:
        print(PRINT_PREPEND + 'Error creating outgoing UNIX socket(s)')
        unix_out = None

    try:
        unix_in = {
            'IN_1'          : UNIX_Coms(UNIX_ADDR_IN_1),
            'IN_2'          : UNIX_Coms(UNIX_ADDR_IN_2),
        }
        [unix_in[key].bind_to_socket() for key in unix_in]
    except:
        print(PRINT_PREPEND + 'Unix sockets not available - continueing without')
        unix = None
        _UNIX_UP = False

    time.sleep(1)

    # send data to a socket
    #unix_out['OUT_1'].send(bytearray('Hello', 'utf-8'))
    #unix_out['OUT_2'].send(bytearray('Sockets!', 'utf-8'))

    # sleep to allow time to receive data from the socket
    time.sleep(1)

     # close all sockets
    #[unix_in[key].close() for key in unix_in]
    #[unix_out[key].close() for key in unix_out]

    print(PRINT_PREPEND + 'Done')

    return 0

if __name__ == '__main__':
    main()
