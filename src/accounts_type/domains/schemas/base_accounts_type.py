from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseAccountsType(BaseModel):
    """Base class used to represent an Account type
    Because, we are using dynamoDB as database and single table design
    it's necessary to define a unique prefix for id: ID_PREFIX

    Attributes
    ----------
    title : str
        a text to print out what the accounts type label
    class_number : int
        the account classification number
    parent_id : str
        the parent id if self is sub / child of an account

    Methods
    -------
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    title: str
    class_number: int
    parent_id: str | None = None

    ID_PREFIX: ClassVar[str] = "aa#"
