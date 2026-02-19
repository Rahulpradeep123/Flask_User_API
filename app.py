from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# persistent storage file
DATA_FILE = 'users.json'

# In-memory database (will be populated from file if available)
users = {}

# helper functions

def load_users():
    global users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
            # JSON keys are strings, convert to ints
            users = {int(k): v for k, v in users.items()}
    else:
        users = {}


def save_users():
    # convert keys to strings for JSON
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in users.items()}, f, indent=2)

# load existing data
load_users()

# Home Route
@app.route('/')
def home():
    return "User API is Running"

# ---------------- GET ----------------
# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id])

# ---------------- POST ----------------
# Add new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = len(users) + 1
    users[user_id] = {
        "name": data["name"],
        "email": data["email"]
    }
    return jsonify({"message": "User added", "user": users[user_id]})

# ---------------- PUT ----------------
# Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"})
    
    data = request.get_json()
    users[user_id]["name"] = data["name"]
    users[user_id]["email"] = data["email"]
    
    return jsonify({"message": "User updated", "user": users[user_id]})

# ---------------- DELETE ----------------
# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"})
    
    deleted_user = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted_user})

if __name__ == '__main__':
    app.run(debug=True)
