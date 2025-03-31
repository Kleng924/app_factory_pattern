from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

def encode_token(customer_id):
    payload = {
        "sub": customer_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None