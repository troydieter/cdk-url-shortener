import os
from aws_cdk import Stack, Environment
from aws_cdk import aws_apigateway, aws_route53, aws_route53_targets, aws_certificatemanager, aws_ec2
from constructs import Construct

# we need default values here since aws-cdk-examples build synthesizes the app
ACCOUNT = os.environ.get('URL_ACCOUNT', 'YOUR_ACCOUNT_ID')
REGION = os.environ.get('URL_REGION', 'YOUR_REGION')
ZONE_NAME = os.environ.get('URL_ZONE_NAME', 'YOUR_ZONE_NAME')
ZONE_ID = os.environ.get('URL_ZONE_ID', 'YOUR_ZONE_ID')
ZONE_CERT = os.environ.get('URL_ZONE_CERT', 'YOUR_CERTIFICATE_ARN')
VPC_ID = os.environ.get('VPC_ID', 'YOUR_VPC_ID')

AWS_ENV = Environment(account=ACCOUNT, region=REGION)


class URLStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, env=AWS_ENV, **kwargs)

        # lookup our pre-created VPC by ID
        self._vpc = aws_ec2.Vpc.from_lookup(self, "vpc", vpc_id=VPC_ID)

    @property
    def URL_vpc(self) -> aws_ec2.IVpc:
        """
            :return: The URL. vpc
            """
        return self._vpc

    def map_URL_subdomain(self, subdomain: str, api: aws_apigateway.RestApi) -> str:
        """
            Maps a sub-domain of URL_ZONE_NAME to an API gateway

            :param subdomain: The sub-domain (e.g. "url")
            :param api: The API gateway endpoint
            :return: The base url (e.g. "https://www.URL_ZONE_NAME.com")
            """
        domain_name = subdomain + '.' + ZONE_NAME
        url = 'https://' + domain_name

        cert = aws_certificatemanager.Certificate.from_certificate_arn(self, 'DomainCertificate', ZONE_CERT)
        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, 'HostedZone',
                                                                         hosted_zone_id=ZONE_ID,
                                                                         zone_name=ZONE_NAME)

        # add the domain name to the api and the A record to our hosted zone
        domain = api.add_domain_name('Domain', certificate=cert, domain_name=domain_name)

        aws_route53.ARecord(
            self, 'UrlShortenerDomain',
            record_name=subdomain,
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGatewayDomain(domain)))

        return url


__all__ = ["URLStack"]
