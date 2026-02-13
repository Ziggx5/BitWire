from flask import Flask, request
import bcrypt

app = Flask(__name__)

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

