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
    #extract the two numbers from the Lambda service's event object
    operation = 'SUBTRACT#'+event['operand1']
    operand1 = int(event['operand1'])
    operand2 = int(event['operand2'])
    lowSubtrahend=0
    highSubtrahend=0
    mathResult=0
    # store the current time in a human readable format in a variable
    now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    #Lookup prerecorded result for current operation 
    # ScanIndexForward=False gives us the dynamodb item with the largest possible exponent recorded for base.
    # Limit=1 ensures that we get one item, at most.
    
    # First, attempt to look up a prerecorded result of operand1+operand2 (SUBTRACT#operand1, operand2, result)
    # In case such a result exists, we retrun it, and exit. 
    rs=table.query(KeyConditionExpression=Key('operation').eq(operation)&Key('operand2').eq(operand2))
    length_rs=len(rs['Items'])
    if length_rs>0:
        mathResult=rs['Items'][0]['result']
        return {
        'statusCode': 200,
        'result': mathResult,
        'body': json.dumps('Your result is ' + str(mathResult))
        }
    else:
        # A prerecorded result did not exist. We check if operand1+0 exists 
        # If not, we add this item (SUBTRACT#operand1,0,operand1)
        rs=table.query(KeyConditionExpression=Key('operation').eq(operation)&Key('operand2').eq(0))
        length_rs=len(rs['Items'])
        if length_rs==0:
            rs=table.put_item(
                Item={
                    'operation': operation,
                    'operand2': 0,
                    'result': operand1,
                    'upd_time': now
                }
        )
    # Now we know the following
    # This item (SUBTRACT#operand1,0,operand1) exixts
    # Items up to (SUBTRACT#operand1,i,operand1+i) may exist, up to operand1+i<operand2
    # Hence, we have table items from which a result may be built.
    #
    # First, if operand2==0, we return the result being operand1, since operand1 + 0 = operand1
    if operand2==0:
        return {
            'statusCode': 200,
            'result': operand1,
            'body': json.dumps('Your result is ' + str(operand1))
        }
    if operand2>0:
        # If operand2 is positive, look up the highest Subtrahend recorded as being subtracted from operand1, in the table
        # (SUBTRACT#operand1, highSubtrahend, result)
        rs=table.query(KeyConditionExpression=Key('operation').eq(operation),ScanIndexForward=False, Limit=1)    

        highSubtrahend=rs['Items'][0]['operand2']
        mathResult=rs['Items'][0]['result']
        # Fill the gap between highSubtrahend and operand2, by inserting items in the table
        for i in range (int(highSubtrahend)+1, int(operand2)+1):
            mathResult=mathResult-1
            rs=table.put_item(
                Item={
                    'operation': operation,
                    'operand2': i,
                    'result': mathResult,
                    'upd_time': now
                }
            )    
    else:
        # If operand2 is negative, look up the lowest subtrahend recorded as being subtracted from operand1, in the table
        # (SUBTRACT#operand1, lowSubtrahend, result)
        rs=table.query(KeyConditionExpression=Key('operation').eq(operation),ScanIndexForward=True, Limit=1)    
        lowSubtrahend=rs['Items'][0]['operand2']
        mathResult=rs['Items'][0]['result']
        # Fill the gap between lowSubtrahend and operand2, by inserting items in the table
        for i in range (int(lowSubtrahend)-1, int(operand2)-1, -1):
            mathResult=mathResult+1
            rs=table.put_item(
                Item={
                    'operation': operation,
                    'operand2': i,
                    'result': mathResult,
                    'upd_time': now
                }
            )    


    # return a properly formatted JSON object
    return {
    'statusCode': 200,
    'result': mathResult,
    'body': json.dumps('Your result is ' + str(mathResult))
    }