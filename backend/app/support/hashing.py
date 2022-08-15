from typing import List

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
