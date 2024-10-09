from dependency_injector.wiring import inject
from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check")
@inject
def health_check():

    return {"message": "OK evrything works fine"}
