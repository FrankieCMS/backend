from typing import Callable, Type

from app.db.connection import engine
from app.support.db.repository import Repository
from sqlmodel import Session


def get_repository(Repo_type: Type[Repository]) -> Callable:
    def get_repo() -> Type[Repository]:
        return Repo_type(session=Session, engine=engine)  # type: ignore

    return get_repo
