from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from shared.infrastructure.containers.app_container import AppContainer
from shared.infrastructure.fastapi.settings import Settings

router = APIRouter()


@router.get("/health-check")
@inject
def health_check(config: Settings = Depends(Provide[AppContainer.config.factory])):

    return {"message": f"OK evrything works fine and version is: {config['version']}"}
