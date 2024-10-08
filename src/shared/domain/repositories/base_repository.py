from abc import ABC, abstractmethod
from typing import Iterable, Optional

from pydantic import BaseModel


class BaseRepository(ABC, BaseModel):
    """Abstract base class for a Repository"""

    @abstractmethod
    def _find_all(
        self, filters: dict, nested: bool = False
    ) -> Optional[Iterable[BaseModel]]:
        raise NotImplementedError()

    @abstractmethod
    def _find_one(self, id: str) -> Optional[BaseModel]:
        raise NotImplementedError()

    @abstractmethod
    def _create(self, other: BaseModel) -> BaseModel:
        raise NotImplementedError()

    @abstractmethod
    def _update(self, id: str) -> Optional[BaseModel]:
        raise NotImplementedError()

    @abstractmethod
    def _delete(self, id: str) -> bool:
        raise NotImplementedError()
