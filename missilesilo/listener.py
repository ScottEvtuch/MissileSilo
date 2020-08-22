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
        self.my_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.my_socket.bind(self.filepath)
        self.my_socket.listen(1)

    def receive(self, timeout=1):
        # Accept connections to my socket
        self.my_connection, client_address = self.my_socket.accept()

        # Receive data sent to us with a 1 second timeout
        # TODO: Actually check the message length provided in the first 4 bytes
        self.my_connection.settimeout(timeout)
        received_data = b''
        try:
            while True:
                received_data += self.my_connection.recv(1024)
        except socket.timeout:
            # Socket timed out, no more data
            pass
        
        return received_data
    
    def respond(self, data):
        # Send the data to the socket
        self.my_connection.send(data)

        # Close the connection
        self.my_connection.close()

    def __init__(self, filepath="/tmp/missilesilo"):
        self.filepath = filepath
