from typing import Callable, Type

from app.db.db import get_db
from app.db.repositories.base import BaseRepository
from fastapi import Depends
from sqlalchemy.orm import Session


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Session = Depends(get_db)) -> Type[BaseRepository]:
        return Repo_type(db)  # type: ignore

    return get_repo
