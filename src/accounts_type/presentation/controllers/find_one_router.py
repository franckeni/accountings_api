import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from accounts_type.domains.usecases.find_one import FindOneUsecase
from accounts_type.presentation.schemas.errors_messages import (
    ErrorMessageAccountsTypeNotFound,
)
from accounts_type.presentation.view_models.accounts_type import ReadAccountsType
from shared.infrastructure.containers.app_container import AppContainer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

find_one_router = APIRouter()


@find_one_router.get(
    "/accounts_type/{id}",
    response_model=ReadAccountsType | bool,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorMessageAccountsTypeNotFound}},
)
@inject
async def find_one_accounts_type(
    id: str,
    find_one_usecase: FindOneUsecase = Depends(
        Provide[AppContainer.find_one_accounts_type_container.factory]
    ),
):
    """Retrieve an Account Type from database with imformation:
    - **id**: required, item must have an id

    :param id: str
    :param get_usecase: Annotated as GetUsecase depends on dependency_injector
     providers factory

    return: Sorted or Null list of Accounts Type
    raise:
    """
    try:
        accounts_type = find_one_usecase(id)

    except AccountsTypeNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exception.message
        )
    except Exception as e:

        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return accounts_type
