from dependency_injector import containers, providers

from accounts_type.presentation.controllers import router as accounts_type
from shared.presentation.controllers.health_check import router as health_check


class RoutesContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide a list of all api routes

    Return:
        List (*args: Injection): _description_
    """

    factory = providers.List(*health_check.routes, *accounts_type.routes)
