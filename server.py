import socket
import threading

HOST = '127.0.0.1'
PORT = 3000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            print(f'{nicknames[clients.index(client)]} diz {msg}')
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)

def receive():
    while True:
        client, adress = server.accept()
        print(f'Conectado com {adress}!')
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname do cliente é {nickname}")
        broadcast(f"{nickname} conectado ao servidor!\n".encode('utf-8'))
        client.send("Conectado ao servidor".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server funcionando...")
receive()