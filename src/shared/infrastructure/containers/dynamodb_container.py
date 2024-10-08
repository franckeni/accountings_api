from dependency_injector import containers, providers

from shared.infrastructure.adapters.dynamodb_table_adapter import DynamodbTableAdapter
from shared.infrastructure.containers.settings_container import SettingsContainer


class DynamodbTableAdapterContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for DynamodbTableAdapter

    Return:
        Factory (provides: ((...) -> DynamodbTableAdapter) | str | None = None,): _description_
    """

    config = SettingsContainer.factory

    factory = providers.Factory(
        DynamodbTableAdapter,
        table_name=config.TABLE_NAME,
        endpoint_url=config.DYNAMODB_URL,
    )
