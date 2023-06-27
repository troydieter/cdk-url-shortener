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
        if target_url is not None:
            return create_short_url(event)

    path_parameters = event.get('pathParameters')
    if path_parameters is not None and path_parameters.get('proxy') is not None:
        return read_short_url(event)

    return {
        'statusCode': 200,
        'body': 'usage: ?targetUrl=URL'
    }


def create_short_url(event):
    target_url = event["queryStringParameters"].get('targetUrl')
    id = str(uuid.uuid4())[:8]
    table = dynamodb.Table(table_name)
    ttl = str(int(time.time()) + 60 * 60 * 24 * 30)  # 30 days
    table.put_item(Item={
        'id': id,
        'target_url': target_url,
        'ttl': ttl
    })
    ttl_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ttl)))
    url = f"https://{event['requestContext']['domainName']}{event['requestContext']['path']}{id}"
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': f"Created URL: {url} with a TTL of {ttl_date}"
    }


def read_short_url(event):
    event_id = event['pathParameters']['proxy']
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'id': event_id})
    item = response.get('Item')
    if item is None:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'No redirect found for {event_id}'
        }
    return {
        'statusCode': 301,
        'headers': {'Location': item.get('target_url')}
    }
