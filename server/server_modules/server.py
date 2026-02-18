import socket
import threading
import json

host = "192.168.1.7"
port = 50505

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

logged_user = None

clients = []
users = {}

def send_message_to_clients(message):
    for client in clients[:]:
        try:
            client.send(json.dumps(message).encode("ascii"))
            print(message)
        except:
            pass

def client_handler(client, address):
    global logged_user
    while True:
        try:
            recv_data = client.recv(1024)

            if not recv_data:
                break

            data = json.loads(recv_data.decode("ascii"))

            if data["type"] == "register":
                username = data["username"]
                password = data["password"]
        
                if username in users:
                    send_json(client, {"type": "register", "status": "fail"})
                    
                else:
                    users[username] = password
                    send_json(client, {"type": "register", "status": "ok"})
                    
            elif data["type"] == "login":
                username = data["username"]
                password = data["password"]

                if users.get(username) == password:
                    logged_user = username
                    clients.append(client)
                    send_json(client, {"type": "login", "status": "ok"})
                else:
                    send_json(client, {"type": "login", "status": "fail"})

            elif data["type"] == "message":
                send_message_to_clients({"type": "message", "user": logged_user, "content": data['content']})
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
        #send_message_to_clients(f"{address} has joined the chat!".encode("ascii"))
        #client.send(f"Connected to the server!".encode("ascii"))

        thread = threading.Thread(target = client_handler, args = (client, address,))
        thread.start()

def send_json(client, data):
    client.send(json.dumps(data).encode("ascii"))

print("server running...")
receive_connection()