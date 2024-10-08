"""AccountsType exception"""


class AccountsTypeNotFoundError(Exception):
    """AccountsTypeNotFoundError is an error that occurs when a accounts type is not found."""

    message = "The accounts type you spcecified does not exist."

    def __str__(self):
        return AccountsTypeNotFoundError.message


class AccountsTypesNotFoundError(Exception):
    """AccountsTypesNotFoundError is an error that occurs when accounts types are not found."""

    message = "No accounts types were found."

    def __str__(self):
        return AccountsTypesNotFoundError.message


class AccountsTypeAlreadyExistsError(Exception):
    """AccountsTypeAlreadyExistsError is an error that occurs when a accounts type with the
    same class number code already exists."""

    message = "The accounts type with the class number you specified already exists."

    def __str__(self):
        return AccountsTypeAlreadyExistsError.message
