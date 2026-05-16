import socket
import threading
import json
import ssl
from PySide6.QtCore import QObject, Signal

class ChatHandler(QObject):
    message_received = Signal(str, str, str)
    users_received = Signal(list)
    server_status = Signal(str)
    profile_picture_received = Signal(str)

    def __init__(self):
        super().__init__()
        self.client = None
        self.running = False
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def connect(self, ip_address, port = 50505):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.settimeout(2)
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
                    
                    if message['type'] == "message":
                        username = message['user']
                        content = message['content']
                        time = message['time']
                        self.message_received.emit(username, content, time)
                    
                    elif message['type'] == "users_list":
                        users = message['content']
                        self.users_received.emit(users)
                        
                    elif message['type'] == "server_status":
                        self.server_status.emit(message['status'])
                        self.handle_disconnect()
                    
                    elif message['type'] == "ping":
                        self.send_json_message({"type": "pong"})
                    
                    elif message['type'] == "message_history":
                        for content in message['content']:
                            self.message_received.emit(content['user'], content['content'], content['time'])
                    
                    elif message['type'] == "profile_picture":
                        self.profile_picture_received.emit(message['content'])

            except socket.timeout:
                continue
            except Exception as e:
                print(str(e))
                self.handle_disconnect()
                break
    
    def send_json_message(self, message):
        if not self.client:
            return
        try:
            self.client.send((json.dumps(message) + "\n").encode("utf-8"))
        except:
            self.handle_disconnect()

    def register(self, username, password, ip_address, encoded_profile_picture):
        try:
            self.connect(ip_address)
            self.send_json_message({
                "type": "register",
                "username": username,
                "password": password,
                "profile_picture": encoded_profile_picture
            })
            response = json.loads(self.client.recv(1024).decode("utf-8"))
            
        except Exception as e:
            self.handle_disconnect()
            return {"type": "error", "message": str(e)}

        self.handle_disconnect()
        return response

    def login(self, username, password, ip_address):
        try:
            self.connect(ip_address)
            self.send_json_message({
                "type": "login",
                "username": username,
                "password": password
            })
            response = json.loads(self.client.recv(1024).decode("utf-8"))
            
            if response["status"] == "ok":
                self.running = True
                threading.Thread(target = self.receive_messages, daemon = True).start()
            else:
                self.handle_disconnect()

        except socket.timeout:
            return {"type": "error", "message": "Server not responding."}
        except Exception as e:
            return {"type": "error", "message": str(e)}
            self.handle_disconnect()

        return response

    def send_message(self, message):
        self.send_json_message({
            "type": "message",
            "content": message
        })
    
    def handle_disconnect(self):
        if not self.client:
            return
            
        self.running = False

        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.client.close()
        except:
            pass

        self.client = None

    def get_profile_pictures(self, username):
        self.send_json_message({"type": "get_profile_picture", "username": username})