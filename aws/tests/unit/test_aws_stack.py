import json
import pytest

from aws_cdk import core
from aws.aws_stack import AwsStack


def get_template():
    app = core.App()
    AwsStack(app, "aws")
    return json.dumps(app.synth().get_stack("aws").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
