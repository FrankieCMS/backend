from datetime import datetime, timedelta
from typing import List

from app.core.config import ACESS_TOKEN_ALGORITHM, SECRET_KEY
from jose import jwt
from passlib.context import CryptContext


class Hashing:

    schemes: List[str] = ["argon2"]

    def __init__(self) -> None:
        self.pwd_context: CryptContext = CryptContext(
            schemes=self.schemes, deprecated="auto"
        )

    def verify_hash(self, plain_text: str, hashed_text: str):
        return self.pwd_context.verify(plain_text, hashed_text)

    def hash(self, text: str):
        return self.pwd_context.hash(text)

    def create_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, key=str(SECRET_KEY), algorithm=str(ACESS_TOKEN_ALGORITHM)
        )
        return encode_jwt

    def decode_token(self, token: str) -> dict[str, str]:
        payload = jwt.decode(
            token, str(SECRET_KEY), algorithms=[str(ACESS_TOKEN_ALGORITHM)]
        )
        return payload
