from dependency_injector import containers, providers

from accounts_type.infrastructures.containers.usecases_containers import (
    CreateAccountsTypeContainer,
    DeleteAccountsTypeContainer,
    FindAllAccountsTypeContainer,
    FindOneAccountsTypeContainer,
    UpdateAccountsTypeContainer,
)
from shared.infrastructure.containers.settings_container import SettingsContainer


class AppContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide auto wiring dependencies
    for all routes
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "accounts_type.presentation.controllers.find_all_router",
            "accounts_type.presentation.controllers.find_one_router",
            "accounts_type.presentation.controllers.create_router",
            "accounts_type.presentation.controllers.update_router",
            "accounts_type.presentation.controllers.delete_router",
            "shared.presentation.controllers.health_check",
        ]
    )
    config = providers.Container(SettingsContainer)

    find_all_accounts_type_container = providers.Container(FindAllAccountsTypeContainer)
    find_one_accounts_type_container = providers.Container(FindOneAccountsTypeContainer)
    create_accounts_type_container = providers.Container(CreateAccountsTypeContainer)
    update_accounts_type_container = providers.Container(UpdateAccountsTypeContainer)
    delete_accounts_type_container = providers.Container(DeleteAccountsTypeContainer)
