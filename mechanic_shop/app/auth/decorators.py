from functools import wraps
from flask import request, jsonify
from .utils import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        user_id = decode_token(token)
        if not user_id:
            return jsonify({"message": "Token is invalid or expired"}), 401
        return f(user_id, *args, **kwargs)
    return decorated