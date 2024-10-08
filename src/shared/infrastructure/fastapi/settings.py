from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str
    admin_email: str
    items_per_user: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DYNAMODB_URL: Optional[str] = None
    DEFAULT_COUNTRY_CODE: int = 33
    TABLE_NAME: str
    production: bool
    allowed_origins: str
