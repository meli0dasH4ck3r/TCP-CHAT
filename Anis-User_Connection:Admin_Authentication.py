def receive_clients(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            if self.is_banned(nickname):
                client.send('BAN'.encode('ascii'))
                client.close()
                continue

            if nickname == 'admin':
                if not self.authenticate_admin(client):
                    continue

            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the Chat'.encode('ascii'))
            client.send('Connected to the Server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def is_banned(self, nickname):
        with open('bans.txt', 'r') as f:
            return nickname + '\n' in f.readlines()

    def authenticate_admin(self, client):
        client.send('PASS'.encode('ascii'))
        password = client.recv(1024).decode('ascii')
        if password != 'password123':
            client.send('REFUSE'.encode('ascii'))
            client.close()
            return False
        return True

        def is_admin(self, client):
            return self.nicknames[self.clients.index(client)] == 'admin'
