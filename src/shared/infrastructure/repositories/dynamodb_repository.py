from typing import Generic, List, Optional, TypeVar

from boto3.dynamodb.conditions import Attr
from pydantic import ConfigDict, PrivateAttr

from accounts_type.presentation.view_models.accounts_type import CreateAccountsType
from shared.domain.repositories.base_repository import BaseRepository
from shared.infrastructure.adapters.dynamodb_table_adapter import DynamodbTableAdapter
from shared.utils.dynamodb_data_transformer import DynamodbDataTransformer
from shared.utils.dynamodb_utils import DynamodbUtils

PARENT_ONLY_LIMIT_ITEMS = 10
WITH_CHILDREN_LIMIT_ITEMS = 100
T = TypeVar("T")


class DynamodbRepository(BaseRepository, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _table_adapter: DynamodbTableAdapter = PrivateAttr()
    _model: T = PrivateAttr()

    def __init__(self, **datas):
        super().__init__(**datas)

        self._table_adapter = datas["table_adapter"]
        self._model = datas["model"]

    @property
    def table(self):
        return self._table_adapter.get_table()

    def _find_all(self, filters: dict, nested: bool = False) -> Optional[List[T]]:
        """Retrieve all item in dynamodb

        Args:
            filters (dict): _description_

        Returns:
            List[T]: _description_
        """
        filter_expression = Attr("pk").begins_with(self._model.ID_PREFIX)
        if filters and "parent_only" in filters and filters["parent_only"] is True:
            filter_expression = filter_expression & Attr("gsi1_pk").not_exists()

        response = self.table.scan(FilterExpression=filter_expression)

        # Getting the last evaluated key for next pagination repsonse
        last_evaluted_key = response.get("LastEvaluatedKey")

        # Paginate returning up to 1MB of data for each iteration
        while last_evaluted_key:
            paginated_response = self.table.scan(
                FilterExpression=filter_expression,
                ExclusiveStartKey=last_evaluted_key,  # To start the iteration from the last evaluation key
            )
            last_evaluted_key = paginated_response.get("LastEvaluatedKey")
            # Extending the result list to include the paginated response
            response["Items"].extend(paginated_response["Items"])

        return [
            self.__format_dynamodb_item_to_schema(item)
            for item in response.get("Items")
        ]

    def _find_one(self, id: str) -> Optional[T]:
        """Find item in dynamodb

        Args:
            id (str): _description_

        Returns:
            T: _description_
        """
        record = self.__get_dynamodb_item(id).get("Item")

        if record is None:
            return None

        return self.__format_dynamodb_item_to_schema(record)

    def _find_with_class_number(self, class_number: str) -> Optional[List[T]]:
        """Find item with class number in dynamodb

        Args:
            id (str): _description_

        Returns:
            T: _description_
        """

        filter_expression = Attr("pk").begins_with(self._model.ID_PREFIX)
        filter_expression = filter_expression & Attr("class_number").eq(class_number)

        return self.table.scan(FilterExpression=filter_expression).get("Items")

    def _create(self, datas: CreateAccountsType) -> T:
        """Save datas to dynamodb

        Args:
            datas (dict): _description_

        Returns:
            T: _description_
        """
        existing_accounts = self._find_with_class_number(datas.class_number)
        if (
            len(existing_accounts) > 0
            and existing_accounts[0].get("class_number") is not None
        ):
            return False

        dynamodb_item = DynamodbDataTransformer.transform(
            datas=datas, entity_prefix=self._model.ID_PREFIX
        )

        self.table.put_item(Item=dynamodb_item)

        return self.__format_dynamodb_item_to_schema(dynamodb_item)

    def _update(self, id: str, datas: dict) -> T:
        """Update datas to dynamodb

        Args:
            id (str): _description_
            datas (dict): _description_

        Returns:
            T: _description_
        """

        record = self.__get_dynamodb_item(id).get("Item")
        if record is None:
            return None

        update_expression = "SET "
        expression_attribute_values = {}

        item_from_dynamodb = self.__format_dynamodb_item_to_schema(record)

        # Filter None values, unsetted values
        modified_values = dict(filter(lambda x: x[1], datas))

        for index, value in enumerate(modified_values):
            separate = "" if index == len(modified_values) - 1 else ", "
            update_expression += f"{value}=:{value}{separate}"
            expression_attribute_values[f":{value}"] = modified_values[value]
            # Set New value in fetched data and return it
            item_from_dynamodb[value] = modified_values[value]

        if DynamodbRepository.__is_update_expression_setted(
            update_expression, expression_attribute_values
        ):
            self.table.update_item(
                Key=DynamodbUtils.key(item_from_dynamodb),
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
            )

        return item_from_dynamodb

    def _delete(self, id: str) -> bool | None:
        """Find item in dynamodb and delete it if exist

        Args:
            id (str): _description_

        Returns:
            bool: _description_
        """
        record = self.__get_dynamodb_item(id).get("Item")

        if record is None:
            return None

        self.table.delete_item(Key=DynamodbUtils.format_key(self._model.ID_PREFIX, id))

        return True

    def __format_dynamodb_item_to_schema(self, record):
        prefix = self._model.ID_PREFIX

        return (
            DynamodbDataTransformer.reverse_transform(record, prefix)
            if "pk" in record.keys()
            else None
        )

    def __get_dynamodb_item(self, id: str):
        return self.table.get_item(
            Key=DynamodbUtils.format_key(self._model.ID_PREFIX, id)
        )

    @staticmethod
    def __is_update_expression_setted(update_expression: str, value: dict) -> bool:
        return (
            (not "SET ".__eq__(update_expression))
            and (not update_expression.isspace())
            and (not {}.__eq__(value))
        )
