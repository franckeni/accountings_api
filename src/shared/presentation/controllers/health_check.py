from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from shared.infrastructure.containers.app_container import AppContainer
from shared.infrastructure.fastapi.settings import Settings

router = APIRouter()


@router.get("/health-check")
@inject
def health_check(config: Settings = Depends(Provide[AppContainer.config.factory])):
    
    version = config.get("version", "0.1.0")

    return {"message": f"OK evrything works fine and version is: {version}"}
