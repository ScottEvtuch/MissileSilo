import socket

class Forwarder():
    def invoke(self, data, timeout=1):
        # Connect to the socket
        my_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        my_socket.connect(self.filepath)

        my_socket.send(data)

        # Receive data sent to us
        my_socket.settimeout(timeout)
        received_data = b''
        try:
            # Get the header and set our expected length
            while len(received_data) < 4:
                received_data += my_socket.recv(1024)
            expected_length = int.from_bytes(received_data[0:4],"big")
            while len(received_data) - 4 < expected_length:
                # Keep receiving data until we get it all
                received_data += my_socket.recv(1024)
            # We've got all the data, return it
        except socket.timeout:
            # Socket timed out, move along
            pass
        
        # Close the socket
        my_socket.close()
        
        return received_data

    def __init__(self, filepath):
        self.filepath = filepath
