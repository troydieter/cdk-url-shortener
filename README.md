
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

The Short URL API allows you to create and access short URLs. You can create a short URL by providing a target URL, and optionally, specify a time-to-live (TTL) for the short URL.

## Usage

To use the Short URL API, you can make HTTP requests with the appropriate parameters. Here's how to interact with the API:

### Create a Short URL

#### Request

To create a short URL, make an HTTP GET request with the following query parameters:

- `targetUrl` (required): The target URL that you want to create a short URL for.
- `ttlEnabled` (optional): Set this parameter to `true` or `false` to enable or disable TTL for the short URL. If not provided, it defaults to `true`.

Example Request:
```
GET /create?url=https://example.com&ttlEnabled=true
```

#### Response

If successful, the API will respond with a short URL and, if TTL is enabled, the TTL expiration date.

Example Response:
```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "text/plain"
    },
    "body": "Created URL: https://shorturl.com/abc123 with a TTL of 2023-09-30 12:00:00"
}
```

### Access a Short URL

#### Request

To access a short URL, simply make an HTTP GET request to the short URL path.

Example Request:
```
GET /abc123
```

#### Response

If the short URL exists and is not expired, the API will respond with a 301 redirection to the target URL. If the short URL does not exist or has expired, a 400 response will be returned.

Example Response (Redirection):
```
HTTP/1.1 301 Moved Permanently
Location: https://example.com
```

Example Response (Short URL Not Found):
```json
{
    "statusCode": 400,
    "headers": {
        "Content-Type": "text/plain"
    },
    "body": "No redirect found for abc123"
}
```

## Example

Here's an example of how to use the Short URL API:

1. Create a Short URL:
   ```
   GET /create?targetUrl=https://example.com&ttlEnabled=true
   ```

2. The API will respond with a short URL. For example:
   ```
   Created URL: https://shorturl.com/abc123 with a TTL of 2023-09-30 12:00:00
   ```

3. Access the Short URL:
   ```
   GET /abc123
   ```

4. The API will redirect you to the target URL (`https://example.com` in this case).

## Error Handling

If there are any errors or issues, the API will respond with appropriate status codes and error messages. Make sure to handle errors based on the response status codes.

## Notes

- The default TTL for a short URL is 30 days, but you can customize it by specifying `ttlEnabled` when creating the short URL.

