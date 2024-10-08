import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeNotFoundError,
)
from accounts_type.domains.usecases.update import UpdateUsecase
from accounts_type.presentation.schemas.errors_messages import (
    ErrorMessageAccountsTypeNotFound,
)
from accounts_type.presentation.view_models.accounts_type import (
    ReadAccountsType,
    UpdateAccountsType,
)
from shared.infrastructure.containers.app_container import AppContainer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

update_router = APIRouter()


@update_router.patch(
    "/accounts_type/{id}",
    response_model=ReadAccountsType,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorMessageAccountsTypeNotFound}},
)
@inject
async def update_accounts_type(
    id: str,
    accounts_type_datas: UpdateAccountsType,
    update_usecase: UpdateUsecase = Depends(
        Provide[AppContainer.update_accounts_type_container.factory]
    ),
):
    """Update an existing Account Type with all the information in accounts_type_datas param:

    - **id**: required, item must have an id
    - **title**: not required
    - **class_number**: not required
    - **parent_id**: not required
    \f
    :param id: Optional boolean, if value is True it mean we want only parents accounts
    :param accounts_type_datas: Optional boolean, if value is True it mean we want only parents accounts
    :param put_usecase: Annotated as PutUsecase depends on dependency_injector
     providers factory

    return: Updated instance of accounts type
    raise:
    """
    try:
        accounts_type = update_usecase(id, accounts_type_datas)

    except AccountsTypeNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exception.message
        )
    except Exception as e:

        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return accounts_type
