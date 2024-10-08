from dependency_injector import containers, providers

from accounts_type.domains.schemas.base_accounts_type import BaseAccountsType
from shared.infrastructure.containers.dynamodb_container import (
    DynamodbTableAdapterContainer,
)
from shared.infrastructure.repositories.dynamodb_repository import DynamodbRepository


class AccountsTypeRepositoryContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide singleton for DynamodbRepository

    Return:
        Factory (provides: ((...) -> DynamodbRepository) | str | None = None,): _description_
    """

    factory = providers.Singleton(
        DynamodbRepository[BaseAccountsType],
        table_adapter=DynamodbTableAdapterContainer.factory,
        model=BaseAccountsType,
    )
