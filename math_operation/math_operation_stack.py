from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins        
    )

from constructs import Construct

class MathOperationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_bucket = s3.Bucket(self, "myBucket")
        my_distribution=cloudfront.Distribution(self, "myDist",
            default_behavior=cloudfront.BehaviorOptions(origin=origins.S3Origin(my_bucket)),
            default_root_object='index.html'
        )
        s3deploy.BucketDeployment(self, "BucketDeployment",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=my_bucket,
            cache_control=[s3deploy.CacheControl.from_string("max-age=31536000,public,immutable")],
            prune=False,
            distribution=my_distribution
        )

        # Create a new DynamoDB table
        mathTable = dynamodb.Table(self, "MathOperationTableTest",
            partition_key=dynamodb.Attribute(
                name="operation",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="operand2",
                type=dynamodb.AttributeType.NUMBER
            ),
            table_name="MathOperationTableTest",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        MathDynamoDBPolicy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'dynamodb:PutItem',
                'dynamodb:DeleteItem',
                'dynamodb:GetItem',
                'dynamodb:Scan',
                'dynamodb:Query',
                'dynamodb:UpdateItem'
            ],
            #resources=['arn:aws:dynamodb:eu-west-1:153065748672:table/MathOperationTableTest']
            resources=[mathTable.table_arn]
        )

        plusFunction = _lambda.Function(
            self, "plusFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="plusFunction.lambda_handler",
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(30)
        )   

        minusFunction = _lambda.Function(
            self, "minusFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="minusFunction.lambda_handler",
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(30)
        )   

        multiplicationFunction = _lambda.Function(
            self, "multiplicationFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="multiplicationFunction.lambda_handler",
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(30),
            environment={
                "plusLambdaArn": plusFunction.function_arn,
                "minusLambdaArn": minusFunction.function_arn
            }
        )   

        divisionFunction = _lambda.Function(
            self, "divisionFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="divisionFunction.lambda_handler",
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(30)
        )   

        exponentialFunction = _lambda.Function(
            self, "exponentialFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="exponentialFunction.lambda_handler",
            code=_lambda.Code.from_asset('lambda'),
            environment={
                "multiplicationLambdaArn": multiplicationFunction.function_arn,
                "plusLambdaArn": plusFunction.function_arn,
                "minusLambdaArn": minusFunction.function_arn
            },
            timeout=Duration.seconds(30)   
        )   

        plusInvokePolicy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'lambda:InvokeFunction',
                'lambda:InvokeAsync'
            ],
            resources=[plusFunction.function_arn]            
        )

        minusInvokePolicy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'lambda:InvokeFunction',
                'lambda:InvokeAsync'
            ],
            resources=[minusFunction.function_arn]            
        )

        multiplicationInvokePolicy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'lambda:InvokeFunction',
                'lambda:InvokeAsync'
            ],
            resources=[multiplicationFunction.function_arn]            
        )

        

        plusFunction.add_to_role_policy(MathDynamoDBPolicy)
        minusFunction.add_to_role_policy(MathDynamoDBPolicy)
        
        multiplicationFunction.add_to_role_policy(MathDynamoDBPolicy)
        multiplicationFunction.add_to_role_policy(plusInvokePolicy)
        divisionFunction.add_to_role_policy(MathDynamoDBPolicy)
        divisionFunction.add_to_role_policy(minusInvokePolicy)
        exponentialFunction.add_to_role_policy(MathDynamoDBPolicy)
        exponentialFunction.add_to_role_policy(multiplicationInvokePolicy)

        base_api = apigateway.RestApi(self, 'MathOperationAPI',
                                  rest_api_name='MathOperationAPI')

        summation_entity = base_api.root.add_resource(
            'summation',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigateway.Cors.ALL_ORIGINS)
        )

        subtraction_entity = base_api.root.add_resource(
            'subtraction',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigateway.Cors.ALL_ORIGINS)
        )

        multiplication_entity = base_api.root.add_resource(
            'multiplication',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigateway.Cors.ALL_ORIGINS)
        )

        division_entity = base_api.root.add_resource(
            'division',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigateway.Cors.ALL_ORIGINS)
        )

        exponential_entity = base_api.root.add_resource(
            'exponential',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=apigateway.Cors.ALL_ORIGINS)
        )

        summation_entity_lambda_integration = apigateway.LambdaIntegration(
            plusFunction,
            proxy=False,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        subtraction_entity_lambda_integration = apigateway.LambdaIntegration(
            minusFunction,
            proxy=False,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        multiplication_entity_lambda_integration = apigateway.LambdaIntegration(
            multiplicationFunction,
            proxy=False,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        division_entity_lambda_integration = apigateway.LambdaIntegration(
            divisionFunction,
            proxy=False,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        exponential_entity_lambda_integration = apigateway.LambdaIntegration(
            exponentialFunction,
            proxy=False,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )


        summation_entity.add_method(
            'POST', summation_entity_lambda_integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        subtraction_entity.add_method(
            'POST', subtraction_entity_lambda_integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        multiplication_entity.add_method(
            'POST', multiplication_entity_lambda_integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        division_entity.add_method(
            'POST', division_entity_lambda_integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        exponential_entity.add_method(
            'POST', exponential_entity_lambda_integration,
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        

 

