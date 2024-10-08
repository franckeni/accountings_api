from dependency_injector import containers, providers

from accounts_type.domains.usecases.create import CreateUsecase
from accounts_type.domains.usecases.delete import DeleteUsecase
from accounts_type.domains.usecases.find_all import FindAllUsecase
from accounts_type.domains.usecases.find_one import FindOneUsecase
from accounts_type.domains.usecases.update import UpdateUsecase
from accounts_type.infrastructures.containers.repository_container import (
    AccountsTypeRepositoryContainer,
)


class FindAllAccountsTypeContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for find all accounts type
    Usecase

    Return:
        Factory (provides: ((...) -> FindAllUsecase) | str | None = None,): _description_
    """

    factory = providers.Factory(
        FindAllUsecase, repo=AccountsTypeRepositoryContainer.factory
    )


class FindOneAccountsTypeContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for find one accounts type
    Usecase

    Return:
        Factory (provides: ((...) -> FindOneUsecase) | str | None = None,): _description_
    """

    factory = providers.Factory(
        FindOneUsecase, repo=AccountsTypeRepositoryContainer.factory
    )


class CreateAccountsTypeContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for create accounts type
    Usecase

    Return:
        Factory (provides: ((...) -> CreateUsecase) | str | None = None,): _description_
    """

    factory = providers.Factory(
        CreateUsecase, repo=AccountsTypeRepositoryContainer.factory
    )


class UpdateAccountsTypeContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for update accounts type
    Usecase

    Return:
        Factory (provides: ((...) -> UpdateUsecase) | str | None = None,): _description_
    """

    factory = providers.Factory(
        UpdateUsecase, repo=AccountsTypeRepositoryContainer.factory
    )


class DeleteAccountsTypeContainer(containers.DeclarativeContainer):
    """Class use to represent the container which provide factory for delete accounts type
    Usecase

    Return:
        Factory (provides: ((...) -> DeleteUsecase) | str | None = None,): _description_
    """

    factory = providers.Factory(
        DeleteUsecase, repo=AccountsTypeRepositoryContainer.factory
    )
