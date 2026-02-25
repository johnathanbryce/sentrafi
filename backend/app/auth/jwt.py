import jwt
import os
from datetime import datetime, timedelta, timezone


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_TIME = 30


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_TIME),
    }
    encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token
