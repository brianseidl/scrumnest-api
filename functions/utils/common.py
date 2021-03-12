# -*- coding: utf-8 -*-
import boto3
import os

DYNAMO_DB_TABLE_NAME = os.environ.get('DYNAMO_DB_TABLE_NAME')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)


def get_stories_by_nest_id(nest_id: str):
    """
    Helper function to query all stories by nest id
    returns: list of stories
    """
    response = table.query(  # TODO: make a helper function with this query
        KeyConditions={
            'nestId': {
                'AttributeValueList': [nest_id],
                'ComparisonOperator': 'EQ'
            },
            'nestComponent': {
                'AttributeValueList': ['STORY'],
                'ComparisonOperator': 'BEGINS_WITH'
            }
        }
    )
    items = response.get("Items", [])

    # add field storyId to all items based on nestComponent
    for item in items:
        item["storyId"] = item["nestComponent"].split('.')[-1]

    return(items)
