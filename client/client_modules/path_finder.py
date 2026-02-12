import sys
import os

def file_root():
    if sys.platform.startswith("lin"):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        picture_path = os.path.join(root, "client_pictures")
        
        return picture_path
