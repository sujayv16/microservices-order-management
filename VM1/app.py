from flask import Flask, jsonify, request
import uuid
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for users (this would usually be a database)
users = {}
# In-memory storage for tokens
tokens = {}

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['GET'])
def get_users():
    """Fetch all users."""
    return jsonify({"users": list(users.values())})

@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user with details."""
    user_data = request.get_json()
    if 'name' not in user_data or 'email' not in user_data or 'password' not in user_data:
        return jsonify({"error": "User name, email, and password are required!"}), 400
    
    # Check if email already exists
    if user_data['email'] in users:
        return jsonify({"error": "Email already in use!"}), 400
    
    user = {
        "id": str(uuid.uuid4()),
        "name": user_data['name'],
        "email": user_data['email'],
        "password_hash": hash_password(user_data['password']),
        "address": user_data.get('address', "Not provided"),
    }
    users[user_data['email']] = user
    return jsonify({"message": f"User {user_data['name']} added successfully!"}), 201

@app.route('/users/login', methods=['POST'])
def login_user():
    """Simple login endpoint to get a token."""
    user_data = request.get_json()
    for user in users.values():
        if user['email'] == user_data['email'] and user['password_hash'] == hash_password(user_data['password']):
            # Generate a token for the user
            token = str(uuid.uuid4())
            tokens[token] = user['email']  # Store token with user email mapping
            return jsonify({"token": token})
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/users/token/<string:token>', methods=['GET'])
def validate_token(token):
    """Validate the token."""
    if token in tokens:
        return jsonify({"valid": True}), 200
    return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

