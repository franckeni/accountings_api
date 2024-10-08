from pydantic import BaseModel

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeAlreadyExistsError,
)
from accounts_type.presentation.view_models.accounts_type import CreateAccountsType
from shared.domain.usecases.base_usecase import BaseUsecase


class CreateUsecase(BaseUsecase):
    """Class used to define a create Usecase

    Attributes
    ----------
    repo: BaseRepository
        Inherited from parent BaseUsecase


    Methods
    -------
    __call__(id: str)
        Auto call function which send the query to find one or null item
    raise: AccountsTypeAlreadyExistsError: Error raised when an accounts type with
    specified class number already exist
    """

    def __call__(self, datas: CreateAccountsType) -> BaseModel:

        result = self._repo._create(datas)

        if result is False:
            raise AccountsTypeAlreadyExistsError()

        return result
