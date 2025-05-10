import os
from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key") # TODO: use later, no need for now

users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    email = data.get('email')

    if not username or not password:
        return jsonify({'error': 'Missing username or password!'}), 400
    if username in users:
        return jsonify({'error': 'Username already exists!'}), 400
    if '@' not in email:
        return jsonify({'error': 'Invalid email format!'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long!'}), 400
    if not full_name:
        return jsonify({'error': 'Missing full name!'}), 400

    pw_hash = generate_password_hash(password)
    profile = {
        'username': username,
        'email': email,
        'full_name': full_name,
        'profile_picture': 'longphanurl.png',
        'bio': 'This is Long Phan!',
        'created_at': int(datetime.now().timestamp())
    }

    users[username] = {'password': pw_hash, 'profile': profile}
    return api_response(data=profile, message='User registered successfully', status=201)

def api_response(data=None, message=None, status=200):
    response = {
        'success': 200 <= status < 300,
        'status': status
    }

    if message:
        response.message = message

    if data is not None:
        response.data = data

    return jsonify(response), status

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
