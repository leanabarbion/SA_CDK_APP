import boto3
import json
import os
import logging

# Configure logging to see in cloud watch
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info("Event: %s", json.dumps(event))

        table_name = os.environ["TABLE"]
        logger.info("DynamoDB: %s", table_name)

        client = boto3.client("dynamodb")

        item_id = event["pathParameters"]["id"]
        logger.info("item_id: %s", item_id)

        response = client.get_item(
            TableName=table_name,
            Key={"id": {"S": item_id}},
        )
        logger.info("get_item response: %s", response)

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"}),
            }

        item = response["Item"]

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "id": item["id"]["S"],
                    "name": item["name"]["S"],
                    "course": item["course"]["S"],
                    "year": item["year"]["S"],
                }
            ),
        }

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }
