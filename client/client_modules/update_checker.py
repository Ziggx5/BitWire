import requests
import os
from packaging import version

current_release = "1.5.0"

def check_update():
    url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
    response = requests.get(url)
    data = response.json()

    try:
        for release in data:
            tag = release["tag_name"]
            if tag.startswith("c"):
                split_release = tag[1:]
                if version.parse(split_release) > version.parse(current_release):
                    latest_release = split_release
                    return latest_release
                    break
                
        return None

    except:
        return None