import socket
import threading
import json

host = "192.168.1.7"
port = 50505

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
users = {}

def send_message_to_clients(message):
    for client in clients[:]:
        try:
            client.send(message)
        except:
            pass

def client_handler(client, address):
    while True:
        try:
            recv_data = client.recv(1024)
            send_message_to_clients(recv_data)

            if not recv_data:
                break

            data = json.loads(recv_data.decode("ascii"))

        except:
            break
    if client in clients:
        clients.remove(client)
    client.close()
    send_message_to_clients(f"{address} left the chat!".encode("ascii"))

def receive_connection():
    while True:
        client, address = server.accept()
        clients.append(client)
        send_message_to_clients(f"{address} has joined the chat!".encode("ascii"))
        client.send(f"Connected to the server!".encode("ascii"))

        thread = threading.Thread(target = client_handler, args = (client, address,))
        thread.start()

print("server running...")
receive_connection()