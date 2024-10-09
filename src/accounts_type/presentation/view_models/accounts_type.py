from typing import Optional

from accounts_type.domains.schemas.base_accounts_type import BaseAccountsType


class ReadAccountsType(BaseAccountsType):
    id: str
    title: str
    class_number: int
    parent_id: str | None = None


class CreateAccountsType(BaseAccountsType):

    id: Optional[str]

    @classmethod
    def create(cls, id_: str, title: str, class_number: int, parent_id: str | None):
        return cls(id_, title, class_number, parent_id)


class UpdateAccountsType(BaseAccountsType):
    id: Optional[str]
    title: Optional[str]
    class_number: Optional[int]
    parent_id: Optional[str] | None = None

    @classmethod
    def create(
        cls,
        id_: Optional[str],
        title: Optional[str],
        class_number: Optional[int],
        parent_id: Optional[str] | None,
    ):
        return cls(id_, title, class_number, parent_id)
