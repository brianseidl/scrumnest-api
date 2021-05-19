# -*- coding: utf-8 -*-
import boto3

from functions.utils.auth import requires_nest_access
from functions.utils.common import USER_POOL_ID
from functions.utils.models import Nest, Story

cog_client = boto3.client("cognito-idp")


@requires_nest_access
def get_nest(event):
    try:
        nest = Nest.get(event['arguments']['nestId'], 'NEST')
    except Nest.DoesNotExist:
        return None

    return nest.to_dict(sprint=event['arguments'].get('sprint'))


def get_nests(event):
    user = (event["identity"] or {}).get("username")
    nests = Nest.scan(Nest.nestComponent == 'NEST')

    # filter nests to ones that user is authorized to access
    nests = filter(lambda nest: user in [nest.owner, *[user['username'] for user in nest.users]], nests)
    return [nest.to_dict() for nest in nests]


@requires_nest_access
def get_story(event):
    try:
        story = Story.get(event["arguments"]["nestId"], f"STORY.{event['arguments']['storyId']}")

    except Story.DoesNotExist:
        return None

    return story.to_dict()


@requires_nest_access
def get_stories(event):
    sprint = event["arguments"].get("sprint")
    if sprint:
        stories = Story.query(event["arguments"]["nestId"], Story.nestComponent.startswith('STORY'), Story.sprint == sprint)
    else:
        stories = Story.query(event["arguments"]["nestId"], Story.nestComponent.startswith('STORY'))

    return [story.to_dict() for story in stories]


def get_users(event):
    prefix = event["arguments"].get("prefix")
    username = event["arguments"].get("username")

    if username:
        user_filter = f'username="{username}"'
    elif prefix:
        user_filter = f'username^="{prefix}"'
    else:
        user_filter = ''

    users = cog_client.list_users(
        UserPoolId=USER_POOL_ID,
        Filter=user_filter
    )

    ret_users = []
    # generate kv attributes bc cognito is weird
    for user in users["Users"]:
        user_dict = {"username": user["Username"]}
        for attr_dict in user["Attributes"]:
            user_dict[attr_dict["Name"]] = attr_dict["Value"]
        ret_users.append(user_dict)

    return ret_users
