class DynamodbUtils:

    @staticmethod
    def key(item: dict):
        return {"pk": item["pk"], "sk": item["sk"]}

    @staticmethod
    def format_key(prefix: str, id: str) -> dict:
        return (
            {
                "pk": f"{prefix}{id}",
                "sk": f"{prefix}{id}",
            }
            if id.find("#") < 0
            else {
                "pk": id,
                "sk": id,
            }
        )
