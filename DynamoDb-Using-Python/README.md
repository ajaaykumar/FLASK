# DynamoDb-Using-Python
## Student Details 
Get and Post data to DynamoDb Using Api Gateway Lambda Python

step1:
open console.aws.amazon.com
to get started with first create a table in DynamoDB
Get into DynamoDB create a table
Table name:
Primary key: 
Primary key is must
Go with the default settings and create table

step2:
now setup api in Api Gateway
getstarted then New api
API name:
Description:
Endpoint Type:Regional
create Api

to add the date in DynamoDB first
create Resource
Resource name:
Resource Path:
click create Resource

under resource
/customer(create a method GET/POST)
POST/GET
then choose integration type
Api gateway supposts different integration type but in this project i am using lambda function 

step 3:
Now Go Head and create a lambda function
Author from scratch
Name:
Runtime:python3.7
Role:
Existing role:





