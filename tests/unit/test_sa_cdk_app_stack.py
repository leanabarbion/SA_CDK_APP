import aws_cdk as core
import aws_cdk.assertions as assertions

from sa_cdk_app.sa_cdk_app_stack import SaCdkAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sa_cdk_app/sa_cdk_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SaCdkAppStack(app, "sa-cdk-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
