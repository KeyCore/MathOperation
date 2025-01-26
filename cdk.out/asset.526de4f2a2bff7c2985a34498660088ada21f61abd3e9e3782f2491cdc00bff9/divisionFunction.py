# import the JSON utility package
import json

# import the AWS SDK (for Python the package name is boto3)
import boto3

# Import dynamodb conditions to be able to express Key conditions in table queries.
from boto3.dynamodb.conditions import Key

# import two packages to help us with dates and date formatting
from time import gmtime, strftime

# create a DynamoDB resource object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
# table = dynamodb.Table('PowerOfMathDatabase')
table = dynamodb.Table('MathOperationTable')

# store the current time in a human readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    client = boto3.client('lambda')
    #extract the two numbers from the Lambda service's event object
    operation = 'DIVIDEND#'+event['operand1']
    dividend = int(event['operand1'])
    divisor = int(event['operand2'])
    highDividend=0
    highResult=0
    mathResult=0
    cnt=0
    # store the current time in a human readable format in a variable
    now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    #Lookup prerecorded result for current operation 
    # ScanIndexForward=False gives us the dynamodb item with the largest possible exponent recorded for base.
    # Limit=1 ensures that we get one item, at most.
    #If divisor is 0, exit computation with an error message.
    if divisor==0:
        return {
            'statusCode': 200,
            'body': json.dumps('Division by 0 is not defined.')
        }
    if dividend%divisor!=0:
        return {
            'statusCode': 200,
            'body': json.dumps('The divisor must be a factor of the dividend: '+str(divisor)+' is not a factor of '+str(dividend))
        }
    # 
    # 
    for i in range(dividend,0,-divisor):
        op='DIVIDEND#'+str(i)
        rs=table.query(KeyConditionExpression=Key('operation').eq(op)&Key('operand2').eq(divisor))
        length_rs=len(rs['Items'])
        if length_rs>0: 
            highDividend=i
            highResult=rs['Items'][0]['result']
            mathResult=highResult+cnt
            break

        cnt=cnt+1

    if mathResult==0:
        mathResult=cnt

    #Rollup
    j=1
    for i in range(highDividend+divisor, dividend+divisor, divisor):
        rs=table.put_item(
            Item={
                'operation': 'DIVIDEND#'+str(i),
                'operand2': divisor,
                'result': highResult+j,
                'upd_time': now
            }
        )
        j=j+1
    
    return {
        'statusCode': 200,
        'result': mathResult,
        'body': json.dumps('Your result is ' + str(mathResult))
        }
