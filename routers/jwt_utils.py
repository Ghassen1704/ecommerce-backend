import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

# Generate JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

import jwt
from fastapi import HTTPException
from datetime import datetime

# Your secret key and algorithm for decoding
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def decode_access_token(token: str):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optionally check expiration or other claims
        if "exp" in payload and payload["exp"] < datetime.utcntiow():
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
