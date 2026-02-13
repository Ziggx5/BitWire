from flask import Flask, request
from flask_socketio import SocketIO
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins = "*")

users = {}

@app.post("/register")
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    users[username] = password
    print(users)

    return {"status": "ok"}, 200

app.run(host = "192.168.1.7", port = 50005, debug = True)

