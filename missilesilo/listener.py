import os
import socket

class Listener():
    def start(self):
        # Make sure the socket does not already exist
        try:
            os.unlink(self.filepath)
        except OSError:
            if os.path.exists(self.filepath):
                raise
        
        # Create a socket and start listening
        print('Binding to {} and listening'.format(self.filepath))
        self.my_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.my_socket.bind(self.filepath)
        self.my_socket.listen(1)

    def receive(self, timeout=1):
        while True:
            # Accept connections to my socket
            if None == self.my_connection:
                print('Waiting for a connection from the client')
                self.my_connection, client_address = self.my_socket.accept()

            # Receive data sent to us
            print('Attempting to receive data from the client')
            self.my_connection.settimeout(timeout)
            received_data = b''
            try:
                # Get the header and set our expected length
                count = 0
                while len(received_data) < 4:
                    received_data += self.my_connection.recv(1024)
                    count += 1
                    if count > 16:
                        # The client has probably left us
                        raise socket.timeout
                expected_length = int.from_bytes(received_data[0:4],"big")
                print('Header received for {} length packet from client'.format(expected_length))
                while len(received_data) - 4 < expected_length:
                    # Keep receiving data until we get it all
                    received_data += self.my_connection.recv(1024)
                # We've got all the data, return it
                print('Full packet received from client')
                break
            except socket.timeout:
                # Socket timed out, close the connection and move along
                print('Client connection timed out, closing connection')
                self.my_connection.close()
                self.my_connection = None
            
        return received_data
    
    def respond(self, data):
        # Send the data to the socket
        print('Sending data to the client')
        self.my_connection.send(data)

    def __init__(self, filepath="/tmp/missilesilo"):
        self.filepath = filepath
        self.my_connection = None
