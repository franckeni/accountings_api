from dataclasses import dataclass
from typing import Final

from accounts_type.domains.entities.value_object.class_number_value_object import (
    ClassNumber,
)
from accounts_type.domains.entities.value_object.id_value_object import Id
from accounts_type.domains.entities.value_object.title_value_object import Title
from shared.domain.entities.entity import AggregateRoot


@dataclass
class AccountsTYpe(AggregateRoot):
    class_number: ClassNumber
    title: Title
    id: Id | None = None
    parent_id: Id | None = None
    ID_PREFIX: Final[str] = "aa#"

    @classmethod
    def create(cls, title: Title, class_number: ClassNumber, id: Id, parent_id: Id):
        return cls(title, class_number, id, parent_id)
