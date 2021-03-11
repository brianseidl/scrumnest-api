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
    pass
