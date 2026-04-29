import socket
import threading
import json
import ssl
import sqlite3
import time
import os
from datetime import datetime
from server_modules.data_manipulation import files_check
from PySide6.QtCore import Signal, QObject

class Client:
    def __init__(self, conn, address):
        self.conn = conn
        self.address = address
        self.username = None
        self.buffer = ""
    
    def send(self, data):
        try:
            self.conn.send((json.dumps(data) + "\n").encode("utf-8"))
        except Exception as e:
            print(e)

class ChatServer(QObject):
    uptime_signal = Signal(int, int, int)

    def __init__(self):
        super().__init__()

        self.host = "0.0.0.0"
        self.port = 50505
        self.clients = []
        self.stop_event = threading.Event()
        self.clients_lock = threading.Lock()

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        self.certfile = None
        self.keyfile = None
        self.database = None

        self.load_files()

    def load_files(self):
        for file_path in files_check():
            if file_path.endswith(".crt"):
                self.certfile = file_path
            elif file_path.endswith(".key"):
                self.keyfile = file_path
            elif file_path.endswith(".db"):
                self.database = file_path

    def init_database(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        """)
        conn.commit()
        conn.close()

    def register_user(self, username, password):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            conn.close()
    
    def login_user(self, username, password):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT password FROM users WHERE username = ?",
                (username,)
            )

            result = cursor.fetchone()

            if result and result [0] == password:
                return True
            return False

        finally:
            conn.close()

    def process_message(self, client, data):
        message_type = data.get("type")

        if message_type == "register":
            username = data.get("username")
            password = data.get("password")

            if not isinstance(username, str) or not isinstance(password, str):
                return

            if self.register_user(username, password):
                client.send({"type": "register", "status": "ok"})
            else:
                client.send({"type": "register", "status": "fail"})

        elif message_type == "login":
            username = data.get("username")
            password = data.get("password")

            if not isinstance(username, str) or not isinstance(password, str):
                return

            if self.login_user(username, password):
                client.username = username
                client.send({"type": "login", "status": "ok"})
                self.add_client(client)
                self.send_users_list(client)
            else:
                client.send({"type": "login", "status": "fail"})
        
        elif message_type == "message":
            if not client.username:
                return

            content = data.get("content")

            if not isinstance(content, str):
                return

            if len(content) > 300:
                return

            current_time = datetime.now().strftime("%l:%M %p, %m/%d/%y")
            self.broadcast({
                "type": "message",
                "user": client.username,
                "content": content,
                "time": current_time
            })
        
        else:
            self.remove_client(client)

    def client_handler(self, client):
        while True:
            try:
                data = client.conn.recv(1024)
                if not data:
                    break

                client.buffer += data.decode("utf-8")

                while "\n" in client.buffer:
                    line, client.buffer = client.buffer.split("\n", 1)

                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                    except:
                        continue

                    if not isinstance(data, dict):
                        break
                    
                    self.process_message(client, data)
            except Exception as e:
                print(e)
                break
        
        self.remove_client(client)
        client.conn.close()


    def start(self):
        if not self.certfile or not self.keyfile or not self.database:
            return

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.stop_event.clear()
        self.context.load_cert_chain(self.certfile, self.keyfile)

        threading.Thread(target = self.server_uptime, daemon = True).start()

        self.init_database()

        while not self.stop_event.is_set():
            try:
                self.server.settimeout(1.0)
                conn, address = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                tls_conn = self.context.wrap_socket(conn, server_side = True)
                client = Client(tls_conn, address)
            except Exception as e:
                print(e)
                conn.close()
                continue

            threading.Thread(target = self.client_handler, args = (client,), daemon = True).start()

    def stop(self):
        self.stop_event.set()

        self.disconnect_all_clients()
        try:
            self.server.close()
        except:
            pass

    def remove_client(self, client):
        with self.clients_lock:
            if client in self.clients:
                self.clients.remove(client)

    def add_client(self, client):
        with self.clients_lock:
            if client not in self.clients:
                self.clients.append(client)

    def disconnect_all_clients(self):
        self.broadcast({"type": "server_status", "status": "Server has been closed."})
            
        with self.clients_lock:
            copy_clients = self.clients[:]
            self.clients.clear()

        for client in copy_clients:
            try:
                client.conn.shutdown(socket.SHUT_RDWR)
            except:
                pass

            try:
                client.conn.close()
            except:
                pass

    def broadcast(self, message):
        with self.clients_lock:
            for client in self.clients[:]:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def send_users_list(self, client):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT username FROM users"
            )
            result = cursor.fetchall()
            users = [user for (user,) in result]
            client.send({"type": "users", "content": users})
        finally:
            conn.close()

    def server_uptime(self):
        start_time = time.time()

        while not self.stop_event.is_set():
            elapsed_time = int(time.time() - start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            self.uptime_signal.emit(hours, minutes, seconds)
            time.sleep(1)