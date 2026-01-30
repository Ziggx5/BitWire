import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 50505))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write_message():
    while True:
        message = f"Ziggx: {input("")}"
        client.send(message.encode("ascii"))

receive_messages_thread = threading.Thread(target = receive_messages)
receive_messages_thread.start()

write_message_thread = threading.Thread(target = write_message)
write_message_thread.start()