import boto3
import json
import os
import logging

# configure logging to see in cloud watch
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info("Event: %s", json.dumps(event))

        table_name = os.environ["TABLE"]
        logger.info("DynamoDB table: %s", table_name)

        client = boto3.client("dynamodb")

        body = json.loads(event["body"])
        logger.info("Body: %s", body)

        required_fields = ["id", "name", "course", "year"]
        for field in required_fields:
            if field not in body:
                return {
                    "statusCode": "400",
                    "body": json.dumps({"message": f"Missing required field: {field}"}),
                }

        item = {
            "id": {"S": body["id"]},
            "name": {"S": body["name"]},
            "course": {"S": body["course"]},
            "year": {"S": body["year"]},
        }

        for key, value in body.items():
            if key not in required_fields:
                item[key] = {"S": value}

        response = client.put_item(TableName=table_name, Item=item)
        logger.info("put_item response: %s", response)

        response_body = {key: value["S"] for key, value in item.items()}

        return {"statusCode": 200, "body": json.dumps(response_body)}

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }
