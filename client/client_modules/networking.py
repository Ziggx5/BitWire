import socket
import threading
import json

class ChatHandler:
    def __init__(self, message_callback):
        self.client = None
        self.running = None
        self.message_callback = message_callback

    def receive_messages(self):
        while self.running:
            message = json.loads(self.client.recv(1024).decode("ascii"))
            complete_message = f"{message['user']}: {message['content']}"
            self.message_callback(complete_message)
            print(complete_message)
            #try:
                #message = json.loads(self.client.recv(1024).decode("ascii"))
                #complete_message = f"{message['user']}: {message['content']}"
                #self.message_callback(complete_message)
            #except:
                #break
        #self.client.close()
    
    def send_json_message(self, message):
        self.client.send(json.dumps(message).encode("ascii"))

    def register(self, username, password, ip_address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, 50505))
        self.send_json_message({
            "type": "register",
            "username": username,
            "password": password
        })
        try:
            response = json.loads(self.client.recv(1024).decode("ascii"))
        except:
            pass
            
        self.client.close()
        return response

    def login(self, username, password, ip_address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, 50505))
        print(self.client)
        self.send_json_message({
            "type": "login",
            "username": username,
            "password": password
        })
        try:
            response = json.loads(self.client.recv(1024).decode("ascii"))
            if response["status"] == "ok":
                print("dela")
                self.running = True
                threading.Thread(target = self.receive_messages, daemon = True).start()
        except:
            pass
        
        return response

    def send_message(self, message):
        self.send_json_message({
            "type": "message",
            "content": message
        })