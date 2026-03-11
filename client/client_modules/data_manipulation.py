from platformdirs import user_data_dir
import os
import json
from cryptography.fernet import Fernet
import base64

def create_local_file():
    app_name = "BitWire"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)

    return data_dir

def key_file():
    data_dir = create_local_file()
    key_path = os.path.join(data_dir, "key.key")
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
    else:
        with open(key_path, "rb") as f:
            key = f.read()
    
    return key

def server_file():
    data_dir = create_local_file()
    server_file_path = os.path.join(data_dir, "servers.json")

    return server_file_path

def identity_file():
    data_dir = create_local_file()
    identity_file_path = os.path.join(data_dir, "identity.json")

    return identity_file_path

def pictures_file():
    data_dir = create_local_file()
    profile_pictures_folder_path = os.path.join(data_dir, "profile_pictures")
    os.makedirs(profile_pictures_folder_path, exist_ok = True)

    return profile_pictures_folder_path

def save_server_data(name, ip_address):
    server_file_path = server_file()
    data = {
        "name": name,
        "ip_address": ip_address
    }
    servers = []

    if os.path.exists(server_file_path):
        with open (server_file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []

    servers.append(data)
        
    with open (server_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)
    
def delete_server(ip_address):
    server_file_path = server_file()
    servers = []

    if os.path.exists(server_file_path):
        with open (server_file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []
        
    for i, server in enumerate(servers):
        if server["ip_address"] == ip_address:
            servers.pop(i)
    
    with open (server_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)

def server_loader():
    file_path = server_file()

    if not os.path.exists(file_path):
        return []

    with open (file_path, "r") as f:
        server_list = json.load(f)
    
    return server_list

def save_identity_data(username, password, profile_picture_path):
    identity_file_path = identity_file()
    key = key_file()
    cipher = Fernet(key)
    encoded_password = password.encode()
    encrypted_password_bytes = cipher.encrypt(encoded_password)
    encrypted_password_string = base64.b64encode(encrypted_password_bytes).decode("utf-8")

    data = {
        "username": username,
        "password": encrypted_password_string,
        "picture_path": profile_picture_path
    }
    identities = []

    if os.path.exists(identity_file_path):
        with open (identity_file_path, "r", encoding = "utf-8") as f:
            try:
                identities = json.load(f)
            except json.JSONDecodeError:
                identities = []
    identities.append(data)

    with open(identity_file_path, "w", encoding = "utf-8") as f:
        json.dump(identities, f, indent = 4)