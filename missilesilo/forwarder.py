import socket

class Forwarder():
    def invoke(self, data, timeout=1):
        # Connect to the socket
        print('Connecting to ssh-agent socket at {}'.format(self.filepath))
        my_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        my_socket.connect(self.filepath)

        print('Sending data to ssh-agent')
        my_socket.send(data)

        # Receive data sent to us
        print('Attempting to receive data from ssh-agent')
        my_socket.settimeout(timeout)
        received_data = b''
        try:
            # Get the header and set our expected length
            while len(received_data) < 4:
                received_data += my_socket.recv(1024)
            expected_length = int.from_bytes(received_data[0:4],"big")
            print('Header received for {} length packet from ssh-agent'.format(expected_length))
            while len(received_data) - 4 < expected_length:
                # Keep receiving data until we get it all
                received_data += my_socket.recv(1024)
            # We've got all the data, return it
            print('Full packet received from ssh-agent')
        except socket.timeout:
            # Socket timed out, we didn't receive the full response
            print('ssh-agent socket timed out, something went wrong')
            raise
        
        # Close the socket
        print('Closing ssh-agent socket')
        my_socket.close()
        
        return received_data

    def __init__(self, filepath):
        self.filepath = filepath
