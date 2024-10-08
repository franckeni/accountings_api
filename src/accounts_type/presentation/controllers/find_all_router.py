import logging
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypesNotFoundError,
)
from accounts_type.domains.usecases.find_all import FindAllUsecase
from accounts_type.presentation.schemas.errors_messages import (
    ErrorMessageAccountsTypesNotFound,
)
from accounts_type.presentation.view_models.accounts_type import ReadAccountsType
from shared.infrastructure.containers.app_container import AppContainer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

find_all_router = APIRouter()


@find_all_router.get(
    "/accounts_type",
    response_model=List[ReadAccountsType],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorMessageAccountsTypesNotFound}},
)
@inject
async def find_all_accounts_type(
    find_all_usecase: FindAllUsecase = Depends(
        Provide[AppContainer.find_all_accounts_type_container.factory]
    ),
    parent_only: Optional[bool] = False,
):
    """Load Accounts Type list from database

    :param parent_only: Optional boolean, if value is True it mean we want only parents accounts
    :param list_usecase: Annotated as FindAllUsecase depends on dependency_injector
     providers factory

    return: Sorted or Null list of Accounts
    raise:
    """

    try:
        # True / False params if we want to fetch children with parent accounts
        parent_only_list = find_all_usecase({"parent_only": parent_only}, False)

    except AccountsTypesNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exception.message
        )
    except Exception as e:

        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Sort accounts type list before, on class_number ASC.
    parent_only_list.sort(key=lambda x: -x["class_number"], reverse=True)

    return parent_only_list
