import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeAlreadyExistsError,
)
from accounts_type.domains.usecases.create import CreateUsecase
from accounts_type.presentation.schemas.errors_messages import (
    ErrorMessageAccountsTypeAlreadyExists,
)
from accounts_type.presentation.view_models.accounts_type import (
    CreateAccountsType,
    ReadAccountsType,
)
from shared.infrastructure.containers.app_container import AppContainer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

create_router = APIRouter()


@create_router.post(
    "/accounts_type",
    response_model=ReadAccountsType,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorMessageAccountsTypeAlreadyExists}
    },
)
@inject
async def create_accounts_type(
    accounts_type_datas: CreateAccountsType,
    create_usecase: CreateUsecase = Depends(
        Provide[AppContainer.create_accounts_type_container.factory]
    ),
):
    """
    Create new Account Type with all the information in accounts_type_datas param:

    - **title**: each item must have a name
    - **class_number**: required number and not already exist
    - **parent_id**: required if it's child of another Accounts Type
    \f
    :param accounts_type_datas: CreateAccountsType
    :param create_usecase: Annotated as CreateUsecase on dependency_injector
     providers factory

    return: The created instance
    raise:
    """

    try:
        accounts_type = create_usecase(accounts_type_datas)

    except AccountsTypeAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exception.message
        )
    except Exception as e:

        logger.error(e)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return accounts_type
