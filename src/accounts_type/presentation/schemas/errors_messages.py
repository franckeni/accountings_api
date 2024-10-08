from pydantic import BaseModel, Field

from accounts_type.domains.exceptions.accounts_type_exceptions import (
    AccountsTypeAlreadyExistsError,
    AccountsTypeNotFoundError,
    AccountsTypesNotFoundError,
)


class ErrorMessageAccountsTypeNotFound(BaseModel):
    detail: str = Field(examples=[AccountsTypeNotFoundError.message])


class ErrorMessageAccountsTypesNotFound(BaseModel):
    detail: str = Field(examples=[AccountsTypesNotFoundError.message])


class ErrorMessageAccountsTypeAlreadyExists(BaseModel):
    detail: str = Field(examples=[AccountsTypeAlreadyExistsError.message])
