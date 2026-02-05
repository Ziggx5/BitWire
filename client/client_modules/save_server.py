from platformdirs import user_data_dir
import os
import json

def save_server_handler(name, ip_address):
    data = {
        "name": name,
        "ip_address": ip_address
    }
    servers = []

    app_name = "BitWire"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)
    servers_file_path = os.path.join(data_dir, "servers.json")

    if os.path.exists(servers_file_path):
        with open (servers_file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []

    servers.append(data)
        
    with open (servers_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)
    