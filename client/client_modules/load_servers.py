import json
from platformdirs import user_data_dir
import os
from client_modules.save_server import save_server_path

def server_loader():
    servers_file_path = save_server_path()

    if not os.path.exists(servers_file_path):
        return []

    with open (servers_file_path, "r") as f:
        server_list = json.load(f)
    
    return server_list