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

        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Item not found"}),
            }

        response = client.delete_item(
            TableName=table_name,
            Key={"id": {"S": item_id}},
        )
        logger.info("delete_item response: %s", response)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Successfully deleted item",
                    "id": item_id,
                }
            ),
        }

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }
