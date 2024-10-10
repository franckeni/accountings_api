from dependency_injector import containers, providers
from fastapi import FastAPI

from shared.infrastructure.containers.app_container import AppContainer
from shared.infrastructure.containers.middleware_container import MiddlewareContainer
from shared.infrastructure.containers.routes_container import RoutesContainer
from shared.infrastructure.containers.settings_container import SettingsContainer


class FastApiContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide the main FastAPI application"""

    config = SettingsContainer.factory

    factory = providers.Singleton(
        FastAPI,
        root_path=config.API_PATH_VERSION_PREFIX,
        openapi_url="/api/v1/openapi.json",
        middleware=MiddlewareContainer.factory,
        container=AppContainer(),
        routes=RoutesContainer.factory,
    )
