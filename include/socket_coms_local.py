#!/usr/bin/python

### * **************************************** * ###
### *   Simple threaded Unix socket server     * ###
### *   running within the payload's container * ###
### * **************************************** * ###
import socket
import os, os.path
import threading
import time

PRINT_PREPEND = '[KINECT LUNA] '
UNIX_SOCKETS_BASE_DIR = '/tmp/payload_sockets/'
UNIX_ADDR_OUT = UNIX_SOCKETS_BASE_DIR + 'pl_sock_a'
UNIX_ADDR_IN = UNIX_SOCKETS_BASE_DIR + 'pl_sock_b'

class UNIX_Coms():

    def __init__(self, host_addr):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server_address = host_addr

    '''
        Creates and binds a new UNIX socket
        Server (listener) side
        - Removes existing socket if it exists
    '''
    def bind_to_socket(self):
        if os.path.exists(self.server_address):
            print(self.server_address);
            os.remove(self.server_address)
        self.sock.bind(self.server_address)
        print(PRINT_PREPEND + 'starting up on {}'.format(self.server_address))
        self.unix_start()

    '''
        Start listening for incoming messages
        sever (listener) side
    '''
    def unix_start(self):
        threading.Thread(target=self.listen).start()

    '''
        Listen for incoming messages (called by unix_start)
    '''
    def listen(self):
        print(PRINT_PREPEND + 'Listening for connections on {}'.format(self.server_address))
        while (True):
            data = self.sock.recv(4096)
            if data:
                # Do something with the data here
                print(PRINT_PREPEND + 'Received data from {} | DATA [{}]: {}'.format(self.server_address, len(data), data))
                cmd = data.decode('utf-8').split('-')
                print(PRINT_PREPEND + 'Capturing K4A Image with following str: ' + cmd[0] + ' t:' + cmd[1])
                params = list(cmd[0])
                fps = params[1]+params[2]
                color = params[3]+params[4]+params[5]+params[6]
                resolution = params[7]+params[8]+params[9]+params[10]
                depth = params[11]

                if fps == '05':
                    fps='5'

                if color == 'BGRA':
                    color = 'BGRA32'
                elif color == 'DP16':
                    color = 'DEPTH16'

                if resolution == '0000':
                    resolution = 'OFF'
                elif resolution == '0720':
                    resolution = '720P'
                else:
                    resolution+='P'

                if depth == '0':
                    depth = 'OFF'
                elif depth == '1':
                    depth = 'NFOV_2X2BINNED'
                elif depth == '2':
                    depth = 'NFOV_UNBINNED'
                elif depth == '3':
                    depth = 'WFOV_2X2BINNED'
                elif depth == '4':
                    depth = 'WFOV_UNBINNED'
                elif depth == '5':
                    depth = 'PASSIVE_IR'

                os.system('../src/check-device -f {} -c {} -r {} -d {} -t {}'.format(fps, color, resolution, depth, cmd[1]))
                #print(PRINT_PREPEND+'check-device -f {} -c {} -r {} -d {} -t {}'.format(fps, color, resolution, depth, cmd[1]))
    '''
        Connects to existing UNIX sockets
        client (sender) side
    '''
    def connect_to_socket(self):
        connect = False
        #while(connect == False):
        try:
            print(PRINT_PREPEND + 'connecting to {}'.format(self.server_address))
            self.sock.connect(self.server_address)
            connect = True
            print(PRINT_PREPEND + 'Connected')
        except socket.error as msg:
            print(msg)

    '''
        Send data to the server
        - connectsto the socket and sends the data
    '''
    def send(self, msg):
        print(PRINT_PREPEND + 'Sending data on socket: {}'.format(self.server_address))

        self.connect_to_socket()
        self.sock.sendall(msg)

    def close(self):
        self.sock.close()
        print(PRINT_PREPEND + 'Socket closed: {}'.format(self.server_address))


def main():

    unix_in  = {}
    unix_out = {}

    try:
        unix_out = {
            'OUT' : UNIX_Coms(UNIX_ADDR_OUT),
        }
    except:
        print(PRINT_PREPEND + 'Error creating outgoing UNIX socket(s)')
        unix_out = None

    try:
        unix_in = {
            'IN'          : UNIX_Coms(UNIX_ADDR_IN),
        }
        [unix_in[key].bind_to_socket() for key in unix_in]
    except:
        print(PRINT_PREPEND + 'Unix sockets not available - continueing without')
        unix = None
        _UNIX_UP = False

    def closeAll():
        [unix_in[key].close() for key in unix_in]
        [unix_out[key].close() for key in unix_out]

    return 0

if __name__ == '__main__':
    main()
