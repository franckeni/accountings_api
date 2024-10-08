from pydantic import BaseModel

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from accounts_type.presentation.view_models.accounts_type import UpdateAccountsType
from shared.domain.usecases.base_usecase import BaseUsecase


class UpdateUsecase(BaseUsecase):
    """Class used to define a update / patch Usecase

    Attributes
    ----------
    repo: BaseRepository
        Inherited from parent BaseUsecase


    Methods
    -------
    __call__(id: str)
        Auto call function which send the query to update item
        by id and custom datas in the repository
    """

    def __call__(self, id: str, datas: UpdateAccountsType) -> BaseModel:

        result = self._repo._update(id, datas)

        if not result:
            raise AccountsTypeNotFoundError()

        return result
