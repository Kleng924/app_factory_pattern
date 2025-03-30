import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps

def encode_token(customer_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_EXPIRATION_TIME']),
        'iat': datetime.utcnow(),
        'sub': customer_id
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to validate the token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            customer_id = decode_token(token)
            if customer_id is None:
                return jsonify({"message": "Invalid token!"}), 401
        except:
            return jsonify({"message": "Invalid token!"}), 401
        
        return f(customer_id, *args, **kwargs)
    
    return decorated