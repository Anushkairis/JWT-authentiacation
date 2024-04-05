from flask import Blueprint, request, jsonify
from verifyToken import generate_token, verify_token
import json

# Creating a Blueprint instance for the authentication-related routes
app = Blueprint('auth_app', __name__)

# Loading user data from userData.json
with open('userData.json', 'r') as json_file:
    users = json.load(json_file)


# Route for user registration
@app.route('/signup', methods=['POST'])
def signup():
    # Extract user registration data from the request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if the username already exists
    if any(user['username'] == username for user in users):
        return jsonify({'message': 'Username already exists'}), 400

    # Add the new user to the userData.json file
    new_user = {'username': username, 'password': password}
    users.append(new_user)

    with open('userData.json', 'w') as file:
        json.dump(users, file, indent=2)

    return jsonify({'message': 'User registered successfully'}), 201


# Route for user login
@app.route('/signin', methods=['POST'])
def signin():
    # Extract user login data from the request
    data = request.get_json()
    username = data.get('username')
    userType = "true"
    password = data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if the provided credentials are valid
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Generate a toke for the authenticated user
        token = generate_token(username, userType)
        return jsonify({'message': 'Login successful', 'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Route for a test page that requires authentication
@app.route('/testPage', methods=['GET'])
def test_page():
    # Extract the token from the request headers
    token = request.headers.get('token')

    # zcheck if the token is provided
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        # Verify the token and extract the username
        username = verify_token(token)
        return jsonify({'message': 'Page accessed', 'username': username})
    except Exception as e:
        return jsonify({'message': str(e)}), 401
