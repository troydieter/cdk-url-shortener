
# AWS CDK (Python) URL Shortener

A fork from this [official AWS sample repository](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/url-shortener), with enhancements!

The project is an implementation of a URL shortener service which demonstrates a few AWS CDK concepts:
- [app.py](./app.py) defines the URL shortener service using AWS Constructs for Lambda, API Gateway and DynamoDB.
- The [url_common](./url_common/__init__.py) module includes a base
  CDK stack class that includes APIs for accessing shared resources such as a
  domain name and a VPC.
- A Time-to-live attribute in AWS DynamoDB, which specifies how long a URL is valid for to be shortened

## Setup

Create and source a Python virtualenv on MacOS and Linux, and install python dependencies:

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Install the latest version of the AWS CDK CLI:

```shell
$ npm i -g aws-cdk
```

The base class depends on the existence of the following environment variables
to find the shared resources (assumed as already deployed):

```shell
export URL_ACCOUNT='1111111111'
export URL_REGION='us-east-1'
export URL_ZONE_NAME='URL.co'
export URL_ZONE_ID='3333333333'
export URL_ZONE_CERT='arn:aws:acm:us-east-1:1111111111:certificate/XYZ-123'
```

## Deployment

At this point, you should be able to deploy all the stacks in this app using:

```shell
$ cdk deploy '*'
```
