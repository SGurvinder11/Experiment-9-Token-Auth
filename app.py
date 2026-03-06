from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "secret123"

# Dummy user credentials
USERNAME = "admin"
PASSWORD = "password"


# Home route
@app.route('/')
def home():
    return "Token Authentication API Running"


# 1️⃣ Authorization Header (Basic Auth)
@app.route('/auth/basic')
def basic_auth():

    auth = request.authorization

    if auth and auth.username == USERNAME and auth.password == PASSWORD:
        return jsonify({"message": "Basic Authentication Successful"})
    
    return jsonify({"message": "Authentication Failed"}), 401


# 2️⃣ Custom Header Authentication
@app.route('/auth/custom')
def custom_auth():

    user = request.headers.get("username")
    pwd = request.headers.get("password")

    if user == USERNAME and pwd == PASSWORD:
        return jsonify({"message": "Custom Header Authentication Successful"})

    return jsonify({"message": "Authentication Failed"}), 401


# 3️⃣ Login → Generate JWT Token
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    if data["username"] == USERNAME and data["password"] == PASSWORD:

        token = jwt.encode({
            "user": data["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


# 4️⃣ JWT Protected Route
@app.route('/auth/jwt')
def jwt_auth():

    auth_header = request.headers.get("Authorization")

    if auth_header:

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({
                "message": "JWT Authentication Successful",
                "user": decoded["user"]
            })

        except:
            return jsonify({"message": "Token invalid"}), 401

    return jsonify({"message": "Token missing"}), 401


if __name__ == "__main__":
    app.run(debug=True)