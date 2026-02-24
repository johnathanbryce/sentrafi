import jwt
import os
from datetime import datetime, timedelta, timezone

SECRET_KEY = "test_secret_key_1"
# TODO: get from .env variable
# SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-very-secure-and-long-secret-key")
ALGORITHM = "HS256"
EXPIRY_TIME = 30


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_TIME),
    }
    encoded_jwt = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    print(f"ENCODED JWT: {encoded_jwt}")
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"DECODED_TOKEN {decoded_token}")
    return decoded_token
