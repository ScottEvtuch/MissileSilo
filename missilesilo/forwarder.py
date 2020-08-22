import socket

class Forwarder():
    def invoke(self, data, timeout=1):
        # Connect to the socket
        my_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        my_socket.connect(self.filepath)

        my_socket.send(data)

        # Receive data sent to us with a 1 second timeout
        # TODO: Actually check the message length provided in the first 4 bytes
        my_socket.settimeout(timeout)
        received_data = b''
        try:
            while True:
                received_data += my_socket.recv(1024)
        except socket.timeout:
            # Socket timed out, no more data
            pass
        
        # Close the socket
        my_socket.close()
        
        return received_data

    def __init__(self, filepath):
        self.filepath = filepath
