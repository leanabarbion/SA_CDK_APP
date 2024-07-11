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

        course = event["pathParameters"]["course"]
        logger.info("Course: %s", course)

        # query to retrieve all items from the same course
        response = client.query(
            TableName=table_name,
            IndexName="course-index",
            KeyConditionExpression="course = :course",
            ExpressionAttributeValues={
                ":course": {"S": course},
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
