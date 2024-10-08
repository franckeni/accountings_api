from typing import Optional

from pydantic import BaseModel

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from shared.domain.usecases.base_usecase import BaseUsecase


class FindOneUsecase(BaseUsecase):
    """Class used to define a get Usecase

    Attributes
    ----------
    repo: BaseRepository
        Inherited from parent BaseUsecase


    Methods
    -------
    __call__(id: str)
        Auto call function which send the query to find one or null item
    """

    def __call__(self, id: str) -> Optional[BaseModel]:

        result = self._repo._find_one(id)

        if not result:
            raise AccountsTypeNotFoundError()

        return result
