from dataclasses import dataclass

from shared.domain.value_object import ValueObject


@dataclass(slots=True)
class Title(ValueObject):
    value: str
