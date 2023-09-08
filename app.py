from aws_cdk import App, Duration, RemovalPolicy
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway
from constructs import Construct
from url_common import URLStack


# our main application stack
class UrlShortenerStack(URLStack):
  def __init__(self, scope: Construct, id: str, **kwarg) -> None:
    super().__init__(scope, id, **kwarg)

    # define the table that maps short codes to URLs.
    table = aws_dynamodb.Table(self, "Table",
                               partition_key=aws_dynamodb.Attribute(
                                 name="id",
                                 type=aws_dynamodb.AttributeType.STRING),
                               billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                               time_to_live_attribute='ttl',
                               encryption=aws_dynamodb.TableEncryption.AWS_MANAGED,
                               point_in_time_recovery=True,
                               removal_policy=RemovalPolicy.DESTROY
                               )

    # define the API gateway request handler. all API requests will go to the same function.
    handler = aws_lambda.Function(self, "UrlShortenerFunction",
                                  code=aws_lambda.Code.from_asset("./lambda"),
                                  handler="handler.main",
                                  timeout=Duration.minutes(5),
                                  runtime=aws_lambda.Runtime.PYTHON_3_9)

    # pass the table name to the handler through an environment variable and grant
    # the handler read/write permissions on the table.
    handler.add_environment('TABLE_NAME', table.table_name)
    table.grant_read_write_data(handler)

    # define the API endpoint and associate the handler
    api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi",
                                       handler=handler)

    # map go.URL.co to this api gateway endpoint
    # the domain name is a shared resource that can be accessed through the API in URLStack
    # NOTE: you can comment this out if you want to bypass the domain name mapping
    self.map_URL_subdomain('io', api)

app = App()
UrlShortenerStack(app, "urlshort-app")

app.synth()
