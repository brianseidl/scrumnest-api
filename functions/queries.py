# -*- coding: utf-8 -*-
import boto3
from boto3.dynamodb.conditions import Key

from functions.utils.common import DYNAMO_DB_TABLE_NAME

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)


def get_nest(event):
    response = table.get_item(Key={'nestId': event["arguments"]["nestId"], 'nestComponent': 'NEST'})
    return(response.get("Item"))


def get_nests(event):
    response = table.scan(FilterExpression=Key('nestComponent').eq('NEST'))
    return(response.get("Items"))


def get_story(event):
    pass


def get_stories(event):
    pass
