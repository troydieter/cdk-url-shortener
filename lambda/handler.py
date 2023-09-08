import os
import uuid
import logging
import time

import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')


def main(event, context):
    logger.info("EVENT: " + str(event))

    query_string_params = event.get("queryStringParameters")
    if query_string_params is not None:
        target_url = query_string_params.get('targetUrl')
        ttl_enabled = query_string_params.get('ttlEnabled', 'true')  # Default to true if not provided
        if target_url is not None:
            return create_short_url(event, ttl_enabled)

    path_parameters = event.get('pathParameters')
    if path_parameters is not None and path_parameters.get('proxy') is not None:
        return read_short_url(event)

    return {
        'statusCode': 200,
        'body': 'usage: ?targetUrl=URL[&ttlEnabled=true|false]'
    }

def create_short_url(event, ttl_enabled):
    target_url = event["queryStringParameters"].get('targetUrl')
    id = str(uuid.uuid4())[:8]
    table = dynamodb.Table(table_name)
    
    if ttl_enabled == 'true':
        ttl = str(int(time.time()) + 60 * 60 * 24 * 30)  # 30 days
    else:
        ttl = None
    
    item = {
        'id': id,
        'target_url': target_url,
    }
    
    if ttl is not None:
        item['ttl'] = ttl
    
    table.put_item(Item=item)
    
    ttl_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ttl))) if ttl else 'N/A'
    
    url = f"https://{event['requestContext']['domainName']}{event['requestContext']['path']}{id}"
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': f"Created URL: {url} with a TTL of {ttl_date}"
    }
