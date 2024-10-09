from accounts_type.domains.schemas.base_accounts_type import BaseAccountsType
from accounts_type.presentation.view_models.accounts_type import ReadAccountsType


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
