from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import jwt


password_hasher = PasswordHash(
    (
        Argon2Hasher(),
    )
)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(
    user_id: str,
    secret_key: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
    }

    token = jwt.encode(payload, secret_key, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(
    token: str,
    secret_key: str,
) -> dict:
    payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM], options={"require": ["sub", "iat", "exp", "type"]})
    return payload