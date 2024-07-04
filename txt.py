import socket
import threading

# made into comment so I can make fixes
# class Server:
#    def __init__(self, host, port):
#        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.server.bind((host, port))
#        self.server.listen()
#        self.clients = []
#        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = input("Choose a nickname: ")
        thread = threading.Thread(target=self.receive)
        thread.start()
        self.write()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('utf-8'))

if __name__ == "__main__":
    choice = input("Type 'server' to start a server or 'client' to connect as a client: ")
    if choice == 'server':
        host = input("Enter host IP: ")
        port = int(input("Enter port number: "))
        server = Server(host, port)
        server.receive()
    elif choice == 'client':
        host = input("Enter host IP: ")
        port = int(input("Enter port number: "))
        client = Client(host, port)
