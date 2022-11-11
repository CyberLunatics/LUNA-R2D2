#!/usr/bin/python

### * ********************************** * ###
### * Simple threaded Unix socket server * ###
### * ********************************** * ###

import socket
import os, os.path
import threading
import time

PRINT_PREPEND = '[socket_coms_1.py] '

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
        




# base location for payload's UNIX sockets
UNIX_SOCKETS_BASE_DIR = '/tmp/payload_sockets/kinect_luna/'
# Outgoing socket(s) (sender)
#   ex: streaming telemetry, store & fwd, reset requests, etc.
UNIX_ADDR_OUT_1 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_1'
UNIX_ADDR_OUT_2 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_2'
# Incoming socket(s) (listener) 
# ex: commands from ground, data from rover, etc.
UNIX_ADDR_IN_1 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_3'
UNIX_ADDR_IN_2 = UNIX_SOCKETS_BASE_DIR + 'pl_sock_4'

        
def main():
    
    unix_in  = {}
    unix_out = {}
    
    # create Outgoing sockets
    # - attempt to connect to existing sockets
    # - socket will be created by rover prior to launching paylaod
    try:
        unix_out = {
            'OUT_1' : UNIX_Coms(UNIX_ADDR_OUT_1),
            'OUT_2' : UNIX_Coms(UNIX_ADDR_OUT_2),
        }
    except:
        print(PRINT_PREPEND + 'Error creating outgoing UNIX socket(s)')
        unix_out = None
    
    # create Incoming sockets
    # - attempt to create & bind to new sockets
    # - socket created by payload application
    try:
        unix_in = {
            'IN_1'          : UNIX_Coms(UNIX_ADDR_IN_1),
            'IN_2'          : UNIX_Coms(UNIX_ADDR_IN_2),
        }
        # FOR EACH: create new sockets, bind to them & starts listening thread
        [unix_in[key].bind_to_socket() for key in unix_in]
    except:
        print(PRINT_PREPEND + 'Unix sockets not available - continueing without')
        unix = None
        _UNIX_UP = False
    
    # sleep to allow sockets to be created by mirror script
    time.sleep(1)
    
    # send data to a socket
    unix_out['OUT_1'].send(bytearray('0x001', 'utf-8'))
    unix_out['OUT_2'].send(bytearray('0x002', 'utf-8'))
    
    # Sleep to allow data to be received on sockets
    time.sleep(1)
    
    # close all sockets
    [unix_in[key].close() for key in unix_in]
    [unix_out[key].close() for key in unix_out]
    
    print(PRINT_PREPEND + 'Done')    
    
    return 0



if __name__ == '__main__':
    main()

