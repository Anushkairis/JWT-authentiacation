import jwt


def generate_token(username, user_type):
    secret_key = 'HELLO'  # Actual secret key
    # Encode the token using JWT with the provided username, user_type and secret key
    return jwt.encode({'username': username, 'user_type': user_type}, secret_key, algorithm='HS256')


def verify_token(token):
    try:
        secret_key = 'HELLO'  # Actual secret key
        # Decode the token using JWT with the provide secret key and verify algorithm
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        print("Decoded Payload:", payload)
        # Extract and return the username and user_type from the decoded payload
        return payload['username'], payload.get('user_type')
    except jwt.ExpiredSignatureError:
        # Handle the case where the token has expired
        raise Exception('Token has expired')
    # Handle the case where the token is invalid
    except jwt.InvalidTokenError as e:
        raise Exception(f'Invalid token: {e}')
