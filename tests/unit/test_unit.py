from dependency_injector import providers

from accounts_type.domains.schemas.base_accounts_type import BaseAccountsType
from accounts_type.domains.usecases.create import CreateUsecase
from accounts_type.domains.usecases.delete import DeleteUsecase
from accounts_type.domains.usecases.find_all import FindAllUsecase
from accounts_type.domains.usecases.find_one import FindOneUsecase
from accounts_type.domains.usecases.update import UpdateUsecase
from accounts_type.infrastructures.containers.repository_container import (
    AccountsTypeRepositoryContainer,
)
from accounts_type.infrastructures.containers.usecases_containers import (
    CreateAccountsTypeContainer,
    DeleteAccountsTypeContainer,
    FindAllAccountsTypeContainer,
    FindOneAccountsTypeContainer,
    UpdateAccountsTypeContainer,
)
from accounts_type.presentation.view_models.accounts_type import ReadAccountsType
from shared.infrastructure.adapters.dynamodb_table_adapter import DynamodbTableAdapter
from shared.infrastructure.containers.app_container import AppContainer
from shared.infrastructure.containers.dynamodb_container import (
    DynamodbTableAdapterContainer,
)
from shared.infrastructure.repositories.dynamodb_repository import DynamodbRepository


def test_base_accounts_type():
    """
    GIVEN an accounts_type
    WHEN BaseAccountsType is inherited
    THEN it has attributes ID_PREFIX with the same value as provided
    """

    accounts_type = BaseAccountsType(
        title="Compte de capitaux",
        class_number="1",
        parent_id=None,
    )

    assert accounts_type.ID_PREFIX == "aa#"


def test_read_accounts_type():
    """
    GIVEN id, title, class_number, parent_id
    WHEN BaseAccountsType is initialized
    THEN it has attributes with the same values as provided
    """

    accounts_type = ReadAccountsType(
        id="c4e24b368ed94ba98fa80eb2722fc5f5",
        title="Compte de capitaux",
        class_number="1",
        parent_id=None,
    )

    assert accounts_type.ID_PREFIX == "aa#"
    assert accounts_type.id == "c4e24b368ed94ba98fa80eb2722fc5f5"
    assert accounts_type.title == "Compte de capitaux"
    assert accounts_type.class_number == 1
    assert accounts_type.parent_id is None


def test_app_container_config():
    app_container = AppContainer()

    config = app_container.config()

    assert isinstance(config.factory, providers.Configuration)
    assert isinstance(config.factory(), dict)


def test_dynamodb_container():
    dynamodb_container = DynamodbTableAdapterContainer()

    dynamodb = dynamodb_container.factory()

    assert isinstance(dynamodb, DynamodbTableAdapter)


def test_repository_container():
    repository_container = AccountsTypeRepositoryContainer()

    repository = repository_container.factory()

    assert isinstance(repository, DynamodbRepository[BaseAccountsType])


def test_find_all_usecase_container():
    find_all_usecase_container = FindAllAccountsTypeContainer()

    find_all_usecase = find_all_usecase_container.factory()

    assert isinstance(find_all_usecase, FindAllUsecase)


def test_find_one_usecase_container():
    find_one_usecase_container = FindOneAccountsTypeContainer()

    find_one_usecase = find_one_usecase_container.factory()

    assert isinstance(find_one_usecase, FindOneUsecase)


def test_create_usecase_container():
    create_usecase_container = CreateAccountsTypeContainer()

    create_usecase = create_usecase_container.factory()

    assert isinstance(create_usecase, CreateUsecase)


def test_update_usecase_container():
    update_usecase_container = UpdateAccountsTypeContainer()

    update_usecase = update_usecase_container.factory()

    assert isinstance(update_usecase, UpdateUsecase)


def test_delete_usecase_container():
    delete_usecase_container = DeleteAccountsTypeContainer()

    delete_usecase = delete_usecase_container.factory()

    assert isinstance(delete_usecase, DeleteUsecase)
