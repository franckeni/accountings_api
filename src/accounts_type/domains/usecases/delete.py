from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from shared.domain.usecases.base_usecase import BaseUsecase


class DeleteUsecase(BaseUsecase):
    """Class used to define a delete Usecase

    Attributes
    ----------
    repo: BaseRepository
        Inherited from parent BaseUsecase


    Methods
    -------
    __call__(id: str)
        Auto call function which send the query to find one or null item
        by id in the repository
    """

    def __call__(self, id: str) -> bool:

        result = self._repo._delete(id)

        if not result:
            raise AccountsTypeNotFoundError()

        return result
