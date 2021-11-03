from aws_cdk import (
    core,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_logs
)


class AwsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_repository = ecr.Repository(self, "ecs-trendr-repository", repository_name="ecs-trendr-repository")
        vpc = ec2.Vpc(self, "ecs-trendr-vpc", max_azs=3)
        cluster = ecs.Cluster(self, "ecs-trendr-cluster", cluster_name="ecs-trendr-cluster", vpc=vpc)
        execution_role = iam.Role(
            self,
            "ecs-trendr-execution-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            role_name="ecs-trendr-execution-role"
        )
        execution_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=["*"],
                actions=[
                    "ecr:GetAuthorizationToken",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ]
            )
        )
        task_definition = ecs.FargateTaskDefinition(
            self,
            "ecs-trendr-task-definition",
            execution_role=execution_role,
            family="ecs-trendr-task-definition"
        )
        container = task_definition.add_container(
            "ecs-trendr-sandbox",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )
        service = ecs.FargateService(
            self,
            "ecs-trendr-service",
            cluster=cluster,
            task_definition=task_definition,
            service_name="ecs-trendr-service",
            assign_public_ip=True
        )
        log_group = aws_logs.LogGroup(self, "ecs-trendr-service-logs-groups", log_group_name="ecs-trendr-service-logs")
        bucket = s3.Bucket(self, "s3-trendr-bucket", bucket_name="s3-trendr-bucket")
