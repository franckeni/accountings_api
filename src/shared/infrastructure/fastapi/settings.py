from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: Optional[str] = None
    version: str
    description: Optional[str] = None
    admin_email: str
    DYNAMODB_URL: Optional[str] = None
    TABLE_NAME: str
    allowed_origins: str
    APP_ENVIRONMENT: str
    API_PATH_VERSION_PREFIX: str
