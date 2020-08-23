import os
from missilesilo.listener import Listener 
from missilesilo.forwarder import Forwarder

class Broker():
    def authenticate(self, query_data):
        # Do whatever we need to do to make sure this request is authorized
        # TODO: Make this actually do something useful
        response_data = self.forwarder.invoke(query_data)
        print('Received data from ssh-agent')
        return response_data

    def passthrough(self, query_data):
        # Forward that data to the forwarder and receive response
        response_data = self.forwarder.invoke(query_data)
        print('Received data from ssh-agent')
        return response_data
    
    def failresponse(self):
        # Generate an SSH agent failure response
        response_data = b'\x00\x00\x00\x01\x05'
        return response_data

    def run(self):
        # Set up our listener
        listener = Listener()
        listener.start()

        # Set up our forwarder
        # TODO: Set up our own SSH agent instead of using the users
        self.forwarder = Forwarder(filepath=os.environ['SSH_AUTH_SOCK'])

        while True:
            # Receive data from the listener
            query_data = listener.receive()

            # Determine the request type
            request_code = query_data[4]

            # Route the request appropriately
            if request_code == 11: #SSH_AGENTC_REQUEST_IDENTITIES
                response_data = self.passthrough(query_data)
            elif request_code == 13: #SSH_AGENTC_SIGN_REQUEST
                response_data = self.authenticate(query_data)
            else: #Something we haven't implemented
                response_data = self.failresponse()

            # Forward the response to the listener
            listener.respond(response_data)
