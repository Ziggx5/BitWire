def receive_messages(ip_address):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_address, 50505))
    print("working")
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
        message = f"User: {input("")}"
        client.send(message.encode("ascii"))

write_message_thread = threading.Thread(target = write_message)
write_message_thread.start()