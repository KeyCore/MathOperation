
# Welcome to the Math Operation - a learning project for serverless web applications
## Storing and resuing results of arithmetic operations with DynamoDB Single Table Design

### Background and Motivation

This project builds an applicaion which can perform the five arithmeic operations summation, subtraction, multiplication, divison and exponential lifting. Common for these five operators is that they are binary, i. e. they take two operands and produce a result. 

operand1 operator operand2 = result 

Examples:

- 6+3 = 9

- 6-3 = 3

- 6*3 = 18

- 6/3 = 2

- 6^3 = 216

 Assume we have only summation (+) and subtraction (-), we would still be able to implement the remaining three oprators. Multiplication, for instance, is a repetition of summation. Division is a repetition of 

- 6*3 = 6 + 6 + 6 (also 6*3 equals 3+3+3+3+3+3+3).

- 6 / 3 = How many times 3 may be subtracted from 6 before reaching 0, which is 2.

- 6^3 = 6 * 6^2 (Exponential can be defined recursively, 6^0=1).

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

- Partition key: *OPERATION#operand1* (String)
- Sort Key: operand2 (Number)

Additional attributes: 
- result (Number)
- upd_time (string)

Examples of items:

| ---	| --- | --- | ---|
| operation | operand2 | result | upd_time |
| ---	| --- | --- | ---|
| ADD#0 | 1 | 1 |Wed, 29 Jan 2025 14:55:45 +0000 |
| ---	| --- | --- | ---|
| ADD#0 | 6 | 6 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|
| ADD#0 | 36 | 36 | Wed, 29 Jan 2025 14:56:43 +0000 |
| ---	| --- | --- | ---|
| ADD#1 | 1 | 2 | Wed, 29 Jan 2025 14:55:46 +0000 |
| ---	| --- | --- | ---|
| ADD#108 | 36 | 144 | Wed, 29 Jan 2025 14:56:43 +0000 |
| ---	| --- | --- | ---|
| ADD#12 | 6 | 18 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|
| ADD#144 | 36 | 180 | Wed, 29 Jan 2025 14:56:43 +0000 |
| ---	| --- | --- | ---|
| ADD#18 | 6 | 24 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|
| ADD#180 | 36 | 216 | Wed, 29 Jan 2025 14:56:43 +0000 |
| ---	| --- | --- | ---|
| ADD#2 | 1 | 3 | Wed, 29 Jan 2025 14:55:46 +0000 |
| ---	| --- | --- | ---|
| ADD#24 | 6 | 30 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|
| ADD#3 | 1 | 4 | Wed, 29 Jan 2025 14:55:46 +0000 |
| ---	| --- | --- | ---|
| ADD#30 | 6 | 36 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|
| ADD#36 | 36 | 72 | Wed, 29 Jan 2025 14:56:43 +0000 |
| ---	| --- | --- | ---|
| ADD#4 | 1 | 5 | Wed, 29 Jan 2025 14:55:46 +0000 |
| ---	| --- | --- | ---|
| ADD#5 | 1 | 6 | Wed, 29 Jan 2025 14:55:46 +0000 |
| ---	| --- | --- | ---|
| ADD#6 | 6 | 12 | Wed, 29 Jan 2025 14:55:47 +0000 |
| ---	| --- | --- | ---|




## Features
- HTML / Javascript / CSS
- API Gateway
- Lambda Functions
- DynamoDB single table design
- CDK - Cloud Development Kit

Fasten your seatbelt, this is going to be fun!

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
