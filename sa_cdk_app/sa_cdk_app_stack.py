import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    RemovalPolicy,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from constructs import Construct


class SaCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self,
            "KnowledgeCatalog",
            partition_key=dynamodb.Attribute(
                name="course", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="name", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )
        table.add_global_secondary_index(
            index_name="id-index",
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
        )
        table.add_global_secondary_index(
            index_name="course-index",
            partition_key=dynamodb.Attribute(
                name="course", type=dynamodb.AttributeType.STRING
            ),
        )
        table.add_global_secondary_index(
            index_name="year-index",
            partition_key=dynamodb.Attribute(
                name="year", type=dynamodb.AttributeType.STRING
            ),
        )

        # Add Item Function
        add_item_func = lambda_.Function(
            self,
            "AddItemFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_add_item"),
            environment={
                "TABLE": table.table_name,
            },
        )
        add_item_func.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem"], resources=[table.table_arn]
            )
        )

        api = apigateway.RestApi(
            self,
            "CatalogApi",
            rest_api_name="Catalog Service",
            description="Knowledge Catalog.",
        )

        items = api.root.add_resource("items")
        items_integration = apigateway.LambdaIntegration(add_item_func)
        items.add_method("POST", items_integration)

        # Delete Item Function
        del_item_func = lambda_.Function(
            self,
            "DeleteItemFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_del_item"),
            environment={
                "TABLE": table.table_name,
            },
        )
        del_item_func.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:DeleteItem", "dynamodb:Query"],
                resources=[table.table_arn, f"{table.table_arn}/index/id-index"],
            )
        )

        del_item = items.add_resource("{id}")
        del_item_integration = apigateway.LambdaIntegration(del_item_func)
        del_item.add_method("DELETE", del_item_integration)

        # Retrieve item Function
        get_item_func = lambda_.Function(
            self,
            "RetrieveItemFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_get_item"),
            environment={
                "TABLE": table.table_name,
            },
        )
        get_item_func.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:GetItem", "dynamodb:Query"],
                resources=[table.table_arn, f"{table.table_arn}/index/id-index"],
            )
        )

        get_item_integration = apigateway.LambdaIntegration(get_item_func)
        del_item.add_method("GET", get_item_integration)

        # Retrieve all items
        get_all_func = lambda_.Function(
            self,
            "RetrieveAllItemFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_get_all"),
            environment={
                "TABLE": table.table_name,
            },
        )
        get_all_func.add_to_role_policy(
            iam.PolicyStatement(actions=["dynamodb:Scan"], resources=[table.table_arn])
        )

        get_all_integration = apigateway.LambdaIntegration(get_all_func)
        items.add_method("GET", get_all_integration)

        # Retrieve items based on course
        get_by_course_func = lambda_.Function(
            self,
            "RetrieveItemByCourseFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_get_by_course"),
            environment={
                "TABLE": table.table_name,
            },
        )
        get_by_course_func.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Query"],
                resources=[f"{table.table_arn}/index/course-index"],
            )
        )

        items_by_course = items.add_resource("course").add_resource("{course}")
        get_by_course_integration = apigateway.LambdaIntegration(get_by_course_func)
        items_by_course.add_method("GET", get_by_course_integration)

        # Retrieve items based on year
        get_by_year_func = lambda_.Function(
            self,
            "RetrieveItemByYearFunction",
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("asset/func_get_by_year"),
            environment={
                "TABLE": table.table_name,
            },
        )
        get_by_year_func.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Query"],
                resources=[f"{table.table_arn}/index/year-index"],
            )
        )

        items_by_year = items.add_resource("year").add_resource("{year}")
        get_by_year_integration = apigateway.LambdaIntegration(get_by_year_func)
        items_by_year.add_method("GET", get_by_year_integration)
