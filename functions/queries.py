# -*- coding: utf-8 -*-
import boto3
from boto3.dynamodb.conditions import Key

from functions.utils.common import DYNAMO_DB_TABLE_NAME, get_stories_by_nest_id

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)


def get_nest(event):
    response = table.get_item(
        Key={
            'nestId': event["arguments"]["nestId"],
            'nestComponent': 'NEST'
        }
    )
    item = response.get("Item")

    if item:
        item["stories"] = get_stories_by_nest_id(item["nestId"])

    return(item)


def get_nests(event):
    response = table.scan(FilterExpression=Key('nestComponent').eq('NEST'))
    items = response.get("Items", [])

    # get the stories associated with each nest
    for item in items:
        item["stories"] = get_stories_by_nest_id(item["nestId"])

    return(items)


def get_story(event):
    response = table.get_item(
        Key={
            'nestId': event["arguments"]["nestId"],
            'nestComponent': f"STORY.{event['arguments']['storyId']}"
        }
    )

    item = response.get("Item")

    if item:
        item["storyId"] = item["nestComponent"].split('.')[-1]

    return(item)


def get_stories(event):
    return get_stories_by_nest_id(event["arguments"]["nestId"])
