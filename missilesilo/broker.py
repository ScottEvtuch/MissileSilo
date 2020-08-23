import os
from missilesilo.listener import Listener 
from missilesilo.forwarder import Forwarder

class Broker():
    def run(self):
        # Set up our listener
        listener = Listener()
        listener.start()

        # Set up our forwarder
        # TODO: Set up our own SSH agent instead of using the users
        forwarder = Forwarder(filepath=os.environ['SSH_AUTH_SOCK'])

        while True:
            # Receive data from the listener
            query_data = listener.receive()

            # TODO: Some sort of logic to route/intercept requests

            # Forward that data to the forwarder and receive response
            response_data = forwarder.invoke(query_data)

            # Forward the response to the listener
            listener.respond(response_data)
