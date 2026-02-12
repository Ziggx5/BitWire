import socket
import threading

class ChatHandler:
    def __init__(self, message_callback):
        self.client = None
        self.running = None
        self.message_callback = message_callback

    def connect_to_server(self, ip_address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_address, 50505))
        self.running = True
        threading.Thread(target = self.receive_messages, daemon = True).start()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode("ascii")
                self.message_callback(message)
            except:
                break
        self.client.close()
    
    def send_message(self, message):
        self.client.send(message.encode("ascii"))