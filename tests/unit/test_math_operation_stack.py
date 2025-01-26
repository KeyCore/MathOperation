import aws_cdk as core
import aws_cdk.assertions as assertions

from math_operation.math_operation_stack import MathOperationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in math_operation/math_operation_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MathOperationStack(app, "math-operation")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
