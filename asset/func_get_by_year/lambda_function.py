import boto3
import json
import os
import logging

# error handling to be found on cloud watch
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info("Event: %s", json.dumps(event))

        table_name = os.environ["TABLE"]
        logger.info("DynamoDB: %s", table_name)

        client = boto3.client("dynamodb")

        year = event["pathParameters"]["year"]
        logger.info("year: %s", year)

        # Query to retrieve all items under the same year
        response = client.query(
            TableName=table_name,
            IndexName="year-index",
            KeyConditionExpression="#yr = :year",
            ExpressionAttributeNames={
                "#yr": "year",
            },
            ExpressionAttributeValues={
                ":year": {"S": year},
            },
        )
        logger.info("query response: %s", response)

        items = response.get("Items", [])

        formatted_items = [
            {k: list(v.values())[0] for k, v in item.items()} for item in items
        ]

        return {
            "statusCode": 200,
            "body": json.dumps(formatted_items),
        }

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }
