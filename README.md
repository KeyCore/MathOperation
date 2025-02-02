
# Math Operation Project - s personal learning project for serverless web applications and DynamoDB Single Table Design

AUTHOR: Kåre J. Kristoffersen, Cloud2@Denmark  
DATE: Feb 2nd, 2025  
LOCATION: Copenhagen,Denmark  

### Background and Motivation

This project builds a serverless web application which can compute arithmetic operations using recursion and a principle of re-using prerecorded subresults in a DynamoDB table with a strict single table design approach.  

The purpose of setting out for this project was to strengten my skills in a couple of areas within AWS. It should be understood literally: To cut it out clearly, I did it alone as a learning project for myself. Now, while this project was not done with the hope that anyone will be using this tiny brower app for any real practical purpose, I will still hope that someone may find it fruitful to use ideas from it.

### A personal Learning project 

For me, this is a learning project!

The learning points I had in mind for this project were these:  
- DynamoDB: Obtain a better understanding DynamoDB Single-Table Design, and also programming using the DynamoDB boto3 API, in this project I choose python.
- CDK scripting: After an earlier attempt to develop a CORS enabled API in CDK, in this project I finally succeeded. Also, in this project, I gained some valuable experience in setting up IAM policies and roles.
- Frontend and Javascript: In 1997 I deveoped a purely static HTML site for a sports club. Yes, hand coded hypertext. That is more or less my front-end experience. Here, In this project, I ony a tiny little to that knowedge, but at east it can retrieve inputs and alert the result back to the user in the browser.  

No matter what, I enjoyed working on this project, hope you find it interesting!  

Fasten your seatbelt, this is going to be fun!

### Artihmetic operations

In this project we are focussing on the five arithmetic operations of summation, subtraction, multiplication, divison and exponential lifting.
Common for the five operators is that they are binary, i. e. they take two operands and produce a result. Hence, the general form is:  

**OPERAND1** **OPERATOR** **OPERAND2** = **RESULT**,  

where **OPERAND1**, **OPERAND2** and **RESULT** are numbers, and **OPERATOR** is one of +,-,*,/ and ^

Examples:

- 6+3 = 9

- 6-3 = 3

- 6*3 = 18

- 6/3 = 2

- 6^3 = 216

### Using recursion, counting and prerecorded subresults
Now, in this project we are **not** going to use the built in arithmetic capabilities of common programming languages. Instead, we are going to implement them using lower operators. To be precise, we will define mutipication in terms of repeated summation, division in terms counting subtraction, and exponential in terms of repeated multiplication. Moreover, we are going to store any computed results, hereby being able to apply a principe of reusing prerecorded subresults.

To see this, assume we have only summation (+) and subtraction (-). Here, we would still be able to implement the remaining three operators. Multiplication, for instance, is repeated summation. 6*3 (six times three), means 6+6+6, and slso 3+3+3+3+3+3, both of which yields 18.

- 6*3 = 6 + 6 + 6 (also 6*3 equals 3+3+3+3+3+3+3).

Division is repeated subtraction of one number from another, while counting how many times it ca be done. 6/3 (6 divided by three) for instance  means asking, how many times may 3 be drawn from 6, and the answer is 2.

- 6 / 3 = How many times 3 may be subtracted from 6 before reaching 0, which is 2.

In the same fashion, exponentials may be computed as repeated multiplication. 6^3 for instance, means 6*6*6. 

- 6^3 = 6 * 6^2. Exponentials can be defined recursively, by noting that the bottom element is 6^0=1.

As stated earlier, in this Math Operation project we will replace:
- multiplication by repeated summation
- division by repeated subtraction
- exponential computation by repeated multiplication (multiplication which is replaced by repeated summation)

The front end programming language in browsers, which is Javascript, of course enables each of the five operators (+,-,*,/,^). However, for the sake of this project let us insist on the following limitations:

- Any computed result of the five operators (+,-,*,/ and ^) must be stored in a way which enables a later reuse of the same result.
- Any request for the computation of any of the five operations must reuse any previously recorded results, which matches the request.
- Only the two built-in operators of summation (+) and ubtracion (-) may be used directly.
- Multiplication (*), Division (/) and exponential (^) should be defined using summation and subtraction.
- Multiplication (*), Division (/) and exponential (^) should be using a principle of reusing also already prerecorded sub-results.

Now, what does it mean to reuse prerecorded sub results? As an example, assume we are interested in computing 6^3, that is six to the power of 3.
First, if we already have the result (216) of that comptation stored, then this should be returnd. And, if we have no exponential computation with base 6 stored, then the result will be computed as multiplying 6 by 6 by 6. Howeve, in case we already have a sub-result for a base 6 exponential, such as 6^2=36, then we may build on that subresult, and say that 6^3 is then 36 multiplied by 6, which gives us 216. Hence, the subresult is reused.

In the same manner we may reuse subresults for multiplication. If we have stored, in DynamoDB, that 6*2 is 12, then 6*3 may be computed as 12 plus 6 which is 18.

In the same manner we may reuse subresults for divison. If we have stored, in DynamoDB, that 3/3 is 1, then 6/3 may be computed as 1+1 which is 2.

### DynamoDB design

We create a DynamoDB table, MathOperationTable, with a composite primary key, as follows:

- Partition key: *OPERATION#operand1* (String)
- Sort Key: operand2 (Number)

Additional attributes: 
- result (Number)
- upd_time (string)

OPERATION = {SUMMATION, SUBTRACTION, MUTIPLICATION, DIVISION, EXPONENTIAL}

Examples: 

The item (SUMMATION#6, 3, 9, 12-01-2025) means that it is recorded that 6+3 is 9, and that this computation was done on Jan 12, 2025.

The item (SUBTRACTION#6, 3, 3, 11-01-2025) means that it is recorded that 6-3 is 3, and that this computation was done on Jan 11, 2025.

The item (MULTIPLICATION#6, 3, 18, 12-01-2025) means that it is recorded that 6*3 is 18, and that this computation was done on Jan 12, 2025.

The item (DIVISIONION#6, 3, 2, 10-01-2025) means that it is recorded that 6/3 is 2, and that this computation was done on Jan 10, 2025.

The item (EXPONENTIAL#6, 3, 216, 12-01-2025) means that it is recorded that 6^3 is 216, and that this computation was done on Jan 12, 2025.

In this way we can see that we may use a single table, in DynamoDB, to represent the five arithmetic operations. 

### Subresults - meaning and usage

With the definition above, we will be able to represent arithmetic operations in such a way that:
1. Existing prerecorded results can be looked up fast. 
2. If a prerecorded result does not exist, then the most appropiate prerecorded subresult mey be effectively identified, and applied in the computation.

Let us see an example of how a prerecorded subresult may help us. Assume we wish to compute the exponential 6^3. 

- First, if an item with partition key 'EXPONENTIAL#6' and sort key of 3 exists the result has indeed be computed earlier, and the result may be looked up and returned directly, as shown below. Here, operation has the value **EXPONENTIAL#6** and exponent is **3**.

 `rs=table.query(KeyConditionExpression=Key('operation').eq(operation)&Key('operand2').eq(exponent))`  
 `Result=rs['Items'][0]['result'] `

- But, if such an item does not exist, then another item with partition key being **EXPONENTIAL#6** and a sort key with a value lower than three may exist, and be helpfull for us. In case it does, we will look it up and reuse it. Hence, we will try to identify the "highest possible prerecorded subresult". Now, what do we mean by the "highest possible prerecorded subresult"? With that we mean the item with partition key 'EXPONENTIAL#6' and then the hightest possible value for the sort key, if such an item exists. Hence, if f. inst an item with partition key 'EXPONENTIAL#6' and sort key 2 exixts, then we will look up that item, in the following way:

`rs=table.query(KeyConditionExpression=Key('operation').eq(operation),ScanIndexForward=False, Limit=1)`

Again, we provide a partition key of value **EXPONENTIAL#6**, but the sort key is not provided. Instead we use ´ScanIndexForward=False´ to  receive the items in decending order based on the sort key. And this is important, since we are interested in the item with the highest sort key. Moreover, we use ´Limit=1´ which makes sure that we only get one single item. We note its result, which is by thew way 36 (6^2 is 36), and then use that result onwards, multiplying it by 6, obtaining the final result, which is then 216.
At this point we insert (put_item) the final resulting item `(EXPONENTIAL#6, 3, 216)` in the table. And by the way, that befiore-mentioned multiplication itself, will be done using a similar recursive principle of reusing its own prerecorded multiplication subresults.

- Finally, what happens if no prerecorded result for EXPONENTIAL#6 exists? In other words, what happens if no exponential with base 6 has been computed earlier? In this case the algorithm will insert these four items in the DynamoDB table, hereby computing the resut bottom-up:

`(EXPONENTIAL#6, 0,   1)`  

`(EXPONENTIAL#6, 1,   6)`  

`(EXPONENTIAL#6, 2,  36)`  

`(EXPONENTIAL#6, 3, 216)`  

These four items will now serve the Math Operation application in these two ways: Any exponential with base 6 and an exponent being three or below may be looked up directly. And, any exponential with base 6 and an exponent being above three may be computed using the prerecorded subresult in the "highest" among the four items namely (EXPONENTIAL#6, 3, 216).

### Accumulative Calculations
With our approach of storing results, and subresults, in DynamoDB, we obtain the fantastic phenomenon, that the more our webapplication is being used, the more arithmetic expressions, and their results, it knows. Hence, the more it is used, the more likeliy it becomes that a requested calculation may be looked up and returnd directly.

### The five Lambda functions

Each of the five Lambda functions receives an event containg two operands, called `operand1`, and `operand1`, and they return a json structure containing the result.

$\lambda$<sub>+</sub>: Summation computes its result by adding the two operands `operand2` from `operand1` directly using the built-in + operator in Python.  
$\lambda$<sub>-</sub>: Subtraction computes its result by subtracting `operand2` from `operand1` directly using the built-in + operator in Python.  
$\lambda$<sub>\*</sub>: Multiplication computes its result by repeated, and counted,  invocations of $\lambda$<sub>+</sub>. Any prerecorded subresult for `MULTIPLICATION#operand1`and a sort key lower than `operand2` will be looked up and reused.  
$\lambda$<sub>\\</sub>: Division computes its result by repeated, and counted,  invocations of $\lambda$<sub>-</sub>.    
$\lambda$<sub>^</sub>: Exponential lifting computes its result by repeated invocations of $\lambda$<sub>*</sub>. Any prerecorded subresult for `EXPONENTIAL#operand1`and a sort key lower than `operand2` will be looked up and reused.  

Remark: In an earlier version, I defined summation and subtraction recursively using repeated operations of adding one (+1) or subtracting 1 (-1) while counting how many times this was done. Now, while this worked well, however, recording the subresults thus obtained, in DynamoDB, made the number of items in the table grow more than I liked.

### Disclaimer
Currently, there is a bug in $\lambda$<sub>\\</sub>. Working on a solution. Suggestions are welcome!

## Features
- HTML / Javascript / CSS
- API Gateway
- Five Lambda Functions
- DynamoDB single table design
- CDK - Cloud Development Kit



This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

## Prerequisites

1. In the file app.py, edit this line to choose your own AWS account id, and the region in which you with to deploy:

    env=cdk.Environment(account="153065748672", region="eu-west-1")

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

At this point you can now deploy the CloudFormation template for this code.

```
$ cdk deploy
```

    env=cdk.Environment(account="153065748672", region="eu-west-1")

## Post Deployment Activities

1. In the file website/apigClient.js locate the line which looks liks this (it should be line 56):

    var invokeUrl = 'Insert the URL for the API generated by CDK in API Gatway here.';

2. Modify that line to conatin the Invoke URL for the API, which has been depoloyed in the deployment process.
The Invoke URL can be found under "stages", and it will have the same structure as the following example:

https://f4fnsy7be4.execute-api.eu-west-1.amazonaws.com/prod

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
