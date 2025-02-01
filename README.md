
# Math Operation Project - a way to learn about serverless web applications

### Background and Motivation

This project builds a serverless web applicaion which can compute the five arithmetic operations summation, subtraction, multiplication, divison and exponential lifting, using a principle of re-using prerecorded subresults in a DynamoDB table with a strict single table design approach. 

Common for the five operators is that they are binary, i. e. they take two operands and produce a result. Hence, the general form is:

<center>
OPERAND1 OPERATOR OPERAND2 = RESULT, 
</center>


where **OPERAND1**, **OPERAND2** and **RESULT** are numbers, and **OPERATOR** is one of +,-,*,/ and ^

Examples:

- 6+3 = 9

- 6-3 = 3

- 6*3 = 18

- 6/3 = 2

- 6^3 = 216

Now, in this project we are not going to use the built in arithmetic capabilities of common programming languages. Instead, we ae going to implement them using lower operators.

To see this, assume we have only summation (+) and subtraction (-). Here, we would still be able to implement the remaining three operators. Multiplication, for instance, is repeated summation. 6*3 (six times three), means 6+6+6, and slso 3+3+3+3+3+3, both of which yields 18.

- 6*3 = 6 + 6 + 6 (also 6*3 equals 3+3+3+3+3+3+3).

Division is repeated subtraction of one number from another, while counting how many times it ca be done. 6/3 (6 divided by three) for instance  means asking, how many times may 3 be drawn from 6, and the answer is 2.

- 6 / 3 = How many times 3 may be subtracted from 6 before reaching 0, which is 2.

In the same fashion, exponentials may be computed as repeated multiplication. 6^3 for instance, means 6*6*6. 

- 6^3 = 6 * 6^2. Exponentials can be defined recursively, by noting that the bottom element is 6^0=1.

In this Math Operation project we will replace:
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

Let us see an example of the usage of a prerecorded subresult. Assume we wish to compute the exponential 6^3. 
- First, if an item with partition key 'EXPONENTIAL#6' and sort key of 3, exists then the result may be looked up and returned directly. 
- But, if such an item does not exist, then we will try to identify the "highest possible prerecorded subresult". Now, what do we mean by the "highest possible prerecorded subresult"? With that we mean the item with partition key 'EXPONENTIAL#6' and then the hightest possible value for the sort key, if such an item exists. Hence, if f. inst an item with partition key 'EXPONENTIAL#6' and sort key 2 exixts, then we will look up that item, note its result, which is 36 (6^2 is 36), and then use that result onwards, multiplying it by 6, obtaining the final result, which is then 216. 
- Finally, what happens if no prerecorded result for EXPONENTIAL#6 exists? In other words, what happens if no exponential with base 6 has been computed earlier? In this case the algorithm will insert these items in the DynamoDB table:

(EXPONENTIAL#6, 0,   1)
(EXPONENTIAL#6, 1,   6)
(EXPONENTIAL#6, 2,  36)
(EXPONENTIAL#6, 3, 216)

These four items will now serve the Math Operation application in these two ways: Any exponential with base 6 and an exponent being three or below may be looked up directly. And, any exponential with base 6 and an exponent being above three may be computed using the prerecorded subresult in the "highest" among the four items namely (EXPONENTIAL#6, 3, 216).



Examples of items:

| operation | operand2 | result | upd_time |
| ---	| --- | --- | ---|
| **ADD#0** | 1 | 1 |Wed, 29 Jan 2025 14:55:45 +0000 |
| **ADD#0** | 6 | 6 | Wed, 29 Jan 2025 14:55:47 +0000 |
| **ADD#0** | 36 | 36 | Wed, 29 Jan 2025 14:56:43 +0000 |
| **ADD#1** | 1 | 2 | Wed, 29 Jan 2025 14:55:46 +0000 |
| **ADD#108** | 36 | 144 | Wed, 29 Jan 2025 14:56:43 +0000 |
| **ADD#12** | 6 | 18 | Wed, 29 Jan 2025 14:55:47 +0000 |
| **ADD#144** | 36 | 180 | Wed, 29 Jan 2025 14:56:43 +0000 |
| **ADD#18** | 6 | 24 | Wed, 29 Jan 2025 14:55:47 +0000 |
| **ADD#180** | 36 | 216 | Wed, 29 Jan 2025 14:56:43 +0000 |
| **ADD#2** | 1 | 3 | Wed, 29 Jan 2025 14:55:46 +0000 |
| **ADD#24** | 6 | 30 | Wed, 29 Jan 2025 14:55:47 +0000 |
| **ADD#3** | 1 | 4 | Wed, 29 Jan 2025 14:55:46 +0000 |
| **ADD#30** | 6 | 36 | Wed, 29 Jan 2025 14:55:47 +0000 |
| **ADD#36** | 36 | 72 | Wed, 29 Jan 2025 14:56:43 +0000 |
| **ADD#4** | 1 | 5 | Wed, 29 Jan 2025 14:55:46 +0000 |
| **ADD#5** | 1 | 6 | Wed, 29 Jan 2025 14:55:46 +0000 |
| **ADD#6** | 6 | 12 | Wed, 29 Jan 2025 14:55:47 +0000 |





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
