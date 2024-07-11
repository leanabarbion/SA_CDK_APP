#!/usr/bin/env python3
import os

import aws_cdk as cdk

from sa_cdk_app.sa_cdk_app_stack import SaCdkAppStack


app = cdk.App()
SaCdkAppStack(app, "SaCdkAppStack",env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    )

app.synth()
