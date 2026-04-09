import socket
import threading
import json
import ssl
from PySide6.QtCore import QObject, Signal

class ChatHandler(QObject):
    message_received = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.client = None
        self.running = False
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def connect(self, ip_address, port = 50505):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tls_socket = self.context.wrap_socket(raw_socket, server_hostname = ip_address)
        tls_socket.connect((ip_address, port))
        self.client = tls_socket

    def receive_messages(self):
        buffer = ""
        while self.running:
            try:
                buffer += self.client.recv(1024).decode("utf-8")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue
                    message = json.loads(line)
                    username = message['user']
                    content = message['content']
                    time = message['time']
                    self.message_received.emit(username, content, time)
                    
            except Exception as e:
                print(str(e))
    
    def send_json_message(self, message):
        self.client.send((json.dumps(message) + "\n").encode("utf-8"))

    def register(self, username, password, ip_address):
        self.connect(ip_address)
        self.send_json_message({
            "type": "register",
            "username": username,
            "password": password
        })
        try:
            response = json.loads(self.client.recv(1024).decode("utf-8"))
        except:
            pass
            
        self.client.close()
        return response

    def login(self, username, password, ip_address):
        self.connect(ip_address)
        self.send_json_message({
            "type": "login",
            "username": username,
            "password": password
        })
        try:
            response = json.loads(self.client.recv(1024).decode("utf-8"))
            if response["status"] == "ok":
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