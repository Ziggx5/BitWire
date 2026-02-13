from server_modules.server import send_message_to_clients, client_handler, receive_connection

def main():
    send_message_to_clients()
    client_handler()
    receive_connection()

if __name__ == "__main__":
    main()