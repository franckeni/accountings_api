import boto3
from pydantic import BaseModel, ConfigDict, PrivateAttr


class DynamodbTableAdapter(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    __table_name: str = PrivateAttr()
    __endpoint_url: str | None = PrivateAttr()

    def __init__(self, table_name: str, endpoint_url: str = None, **datas):
        super().__init__(**datas)

        self.__table_name = table_name
        self.__endpoint_url = endpoint_url

    @classmethod
    def create(cls, table_name: str, endpoint_url: str):
        return cls(table_name, endpoint_url)

    def get_dynamodb(self):
        return boto3.resource(
            "dynamodb",
            endpoint_url=self.__endpoint_url,
        )

    def get_table(self):
        return self.get_dynamodb().Table(name=self.__table_name)
