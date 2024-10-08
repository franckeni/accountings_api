import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from accounts_type.domains.usecases.delete import DeleteUsecase
from accounts_type.presentation.schemas.errors_messages import (
    ErrorMessageAccountsTypeNotFound,
)
from shared.infrastructure.containers.app_container import AppContainer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


delete_router = APIRouter()


@delete_router.delete(
    "/accounts_type/{id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorMessageAccountsTypeNotFound}},
)
@inject
async def delete_accounts_type(
    id: str,
    delete_usecase: DeleteUsecase = Depends(
        Provide[AppContainer.delete_accounts_type_container.factory]
    ),
):
    """Delete an Account Type in database with id information

    - **id**: required, item must have an id

    :param id: str
    :param delete_usecase: Annotated as DeleteUsecase depends on dependency_injector
     providers factory

    return: boolean, True if the account has been removed correctly
    raise:
    """
    try:
        result = delete_usecase(id)

    except AccountsTypeNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exception.message
        )
    except Exception as e:

        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return result
