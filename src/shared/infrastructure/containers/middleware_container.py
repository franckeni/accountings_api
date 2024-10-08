from dependency_injector import containers, providers
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from shared.infrastructure.containers.settings_container import SettingsContainer


class MiddlewareContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for a list of Middleware

    Return:
        List (*args: Injection): _description_
    """

    config = SettingsContainer.factory

    allow_origin = f"{config.allowed_origins()}".split(",")

    header_value = {"allowed_origin": allow_origin}

    factory = providers.List(
        Middleware(
            CORSMiddleware,
            allow_origins=allow_origin,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )
