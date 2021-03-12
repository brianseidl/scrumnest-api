# -*- coding: utf-8 -*-
import boto3
import ulid
from datetime import datetime

from functions.utils.common import DYNAMO_DB_TABLE_NAME

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)


def create_nest(event):
    """
    createNest function to create a nest object in the dynamodb table
    """
    item = {
        'nestId': ulid.new().str,
        'nestComponent': 'NEST',
        'createdAt': str(datetime.now()),
        'name': event["arguments"].get("name", ""),
        'owner': (event["identity"] or {}).get("username"),
        'users': []
    }
    table.put_item(Item=item)

    return(item)


def add_nest_user(event):
    response = table.update_item(
        Key={'nestId': event["arguments"]["nestId"], 'nestComponent': 'NEST'},
        UpdateExpression="SET #usrs = list_append(#usrs, :i)",
        ExpressionAttributeNames={
            '#usrs': 'users',
        },
        ExpressionAttributeValues={
            ':i': [event["arguments"]["username"]],
        },
        ReturnValues='ALL_NEW'
    )
    return response["Attributes"]


def create_story(event):
    # first get nest so we know it exists
    response = table.get_item(Key={'nestId': event["arguments"]["nestId"], 'nestComponent': 'NEST'})
    response["Item"]  # this will throw an error if nest does not exist  TODO: make this nicer

    story_id = ulid.new().str

    # now that we know that the nest exists, lets add the item
    item = {
        'nestId': event["arguments"]["nestId"],
        'nestComponent': f"STORY.{story_id}",
        'createdAt': str(datetime.now()),
        'title': event["arguments"]["title"],
        'description': event["arguments"].get("descritpion"),
        'owner': event["arguments"].get("owner"),
        'status': event["arguments"].get("status", "IDEA")
    }
    table.put_item(Item=item)

    item["storyId"] = story_id
    return(item)
