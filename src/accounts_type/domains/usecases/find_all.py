from typing import Iterable, Optional

from pydantic import BaseModel

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypesNotFoundError,
)
from shared.domain.usecases.base_usecase import BaseUsecase


class FindAllUsecase(BaseUsecase):
    """Class used to define a list Usecase

    Attributes
    ----------
    repo: BaseRepository
        Inherited from parent BaseUsecase


    Methods
    -------
    __call__(filters: dict, nested: bool = False)
        Auto call function which send the query to fetch all / load list or null items
    """

    def __call__(
        self, filters: dict, nested: bool = False
    ) -> Optional[Iterable[BaseModel]]:

        result = self._repo._find_all(filters, nested)

        if not result:
            raise AccountsTypesNotFoundError()

        return result
