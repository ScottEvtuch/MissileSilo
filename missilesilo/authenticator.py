class Authenticator():
    def gather_info(self, query_data):                
        # Determine the length of the keyblob and grab its format
        keyblob_length = int.from_bytes(query_data[6:9],"big")
        keyblob_end = keyblob_length + 9
        keyformat_length = int.from_bytes(query_data[10:13],"big")
        keyformat = query_data[13:13+keyformat_length].decode("utf-8")
        public_key = query_data[13+keyformat_length+4:keyblob_end]
        print('Key format is {}'.format(keyformat))

        # Determine the length of the data section
        data_start = keyblob_end +1
        data_length = int.from_bytes(query_data[data_start:data_start+3],"big")
        nonce_length = int.from_bytes(query_data[data_start+4:data_start+7],"big")

        # Let's try to figure out the username by assuming it comes after the nonce
        username_start = data_start+9+nonce_length
        username_length_bytes = query_data[username_start:username_start+3]
        username_length = int.from_bytes(username_length_bytes,"big")
        username_end = username_start + username_length + 3
        username = query_data[username_start+3:username_end].decode("utf-8")
        print('Request is for username: {}'.format(username))

        return {
            'format': keyformat,
            'username': username,
        }

    def authenticate(self, query_data):
        # TODO: Have this actually authenticate the request
        self.gather_info(query_data)
        return True
