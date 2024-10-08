from dependency_injector import containers, providers

from shared.infrastructure.fastapi.settings import Settings


class SettingsContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide global configuration
    to other providers from with loaded configuration file and the Settings class
    """

    json_config = Settings().model_dump(mode="json")
    factory = providers.Configuration()
    factory.from_dict(json_config)
