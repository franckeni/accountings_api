from fastapi import FastAPI
from mangum import Mangum

from shared.infrastructure.containers.fastapi_container import FastApiContainer


# if __name__ == "__main__":
def create_app() -> FastAPI:
    api = FastApiContainer().factory()

    return api


api = create_app()
handler = Mangum(api)
