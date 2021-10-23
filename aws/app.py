#!/usr/bin/env python3

from aws_cdk import core

from aws.aws_stack import AwsStack


app = core.App()
AwsStack(app, "aws", env=core.Environment(account="514592108082", region="us-east-2"))

app.synth()
