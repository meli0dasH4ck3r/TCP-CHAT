import threading
import socket

class ChatServer:
    def __init__(self, host="127.0.0.1", port=5555):
        # Initialize server and configure socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.commands = {
            "KICK": self.kick_command,
            "BAN": self.ban_command
        }
        print("Server is Listening ...")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        # Handle client's message (could be an admin or regular message)
        while True:
            try:
                msg = client.recv(1024).decode('ascii')
                command, *args = msg.split(" ", 1)
                if command in self.commands:
                    self.commands[command](client, *args)
                else:
                    self.broadcast(msg.encode('ascii'))
            except socket.error:
                self.disconnect_client(client)
                break

    def kick_command(self, client, name):
        # Handle 'kick' command for admin
        if self.is_admin(client):
            self.kick_user(name)
        else:
            client.send('Command Refused!'.encode('ascii'))

    def ban_command(self, client, name):
        # Handle 'ban' command for admin -> add to bans.txt
        if self.is_admin(client):
            self.kick_user(name)
            with open('bans.txt', 'a') as f:
                f.write(f'{name}\n')
            print(f'{name} was banned by the Admin!')
        else:
            client.send('Command Refused!'.encode('ascii'))

    def kick_user(self, name):
        if name in self.nicknames:
            name_index = self.nicknames.index(name)
            client_to_kick = self.clients[name_index]
            self.clients.remove(client_to_kick)
            client_to_kick.send('You Were Kicked from Chat!'.encode('ascii'))
            client_to_kick.close()
            self.nicknames.remove(name)
            self.broadcast(f'{name} was kicked from the server!'.encode('ascii'))

    def disconnect_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            client.close()
            nickname = self.nicknames.pop(index)
            self.broadcast(f'{nickname} left the Chat!'.encode('ascii'))