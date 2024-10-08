import uuid

from pydantic import BaseModel

from shared.domain.entities.dynamodb_item import DynamodbItem


class DynamodbDataTransformer:

    @staticmethod
    def transform(datas: BaseModel, entity_prefix: str) -> DynamodbItem:
        """
        Transform datas BaseModel sent from à POST to DynamodbItem
        Create and Set the id with uuid 4
        id and parent_id keys are not setted or are removed

        Args:
            datas (BaseModel): _description_
            entity_prefix (str): The prefix of item id stored in dynamodb

        Returns:
            DynamodbItem: _description_
        """

        dynamodb_item = DynamodbItem.from_dict(
            pk=(
                f"{entity_prefix}{uuid.uuid4().hex}"
                if not hasattr(datas, "id") or (not datas.id)
                else DynamodbDataTransformer.__transform_id(
                    str(datas.id), entity_prefix
                )
            ),
            gsi1_pk=(
                f"{entity_prefix}{datas.parent_id}"
                if (hasattr(datas, "parent_id")) and (datas.parent_id is not None)
                else None
            ),
        )

        return dynamodb_item.to_dict(datas.model_dump(exclude="parent_id"))

    @staticmethod
    def reverse_transform(dynamodb_item: DynamodbItem, entity_prefix: str) -> dict:
        """
        reverse Transform datas from DynamodbItem to BaseModel

        Args:
            datas (DynamodbItem): _description_

        Returns:
            BaseModel: _description_
        """
        base_model_id = (
            dynamodb_item["pk"].split(entity_prefix)[1]
            if dynamodb_item["pk"].startswith(entity_prefix)
            else dynamodb_item["pk"]
        )

        base_model = {"id": base_model_id}

        if "gsi1_pk" in dynamodb_item and dynamodb_item["gsi1_pk"] is not None:
            base_model["parent_id"] = (
                dynamodb_item["gsi1_pk"].split(entity_prefix)[1]
                if dynamodb_item["gsi1_pk"].startswith(entity_prefix)
                else dynamodb_item["gsi1_pk"]
            )

        return {**base_model, **dynamodb_item}

    @staticmethod
    def __transform_id(id: str, entity_prefix: str):
        return f"{entity_prefix}{id}" if (id.find("#") < 0 and len(id)) > 3 else id
