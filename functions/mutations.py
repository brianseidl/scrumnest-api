# -*- coding: utf-8 -*-
import ulid

from functions.utils.auth import requires_nest_access, requires_nest_ownership
from functions.utils.models import Nest, Story, Attachment


def create_nest(event):
    """
    createNest function to create a nest object in the dynamodb table
    """
    nest = Nest(
        ulid.new().str,
        'NEST',
        name=event["arguments"].get("name", ""),
        owner=(event["identity"] or {}).get("username"),
        users=[]
    )
    nest.save()

    return nest.to_dict()


@requires_nest_ownership
def add_nest_user(event):
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')
    users = list(nest.users)
    users.append(event["arguments"]["username"])
    nest.users = users

    return nest.to_dict()


@requires_nest_access
def create_story(event):
    # get nest so we know it exists first
    Nest.get(event["arguments"]["nestId"], 'NEST')

    story = Story(
        event["arguments"]["nestId"],
        f'STORY.{ulid.new().str}',
        title=event["arguments"]["title"],
        description=event["arguments"].get("descritpion"),
        owner=event["arguments"].get("owner") or (event["identity"] or {}).get("username"),
        status=event["arguments"].get("status", "IDEA")
    )
    story.save()

    return story.to_dict()


@requires_nest_access
def add_story_attachment(event):
    # get story so we know it exists first
    story = Story.get(event["arguments"]["nestId"], f"STORY.{event['arguments']['storyId']}")
    new_attachment = Attachment(
        name=event["arguments"]["name"],
        key=event["arguments"]["key"]
    )
    story.attachments.append(new_attachment)
    story.save()

    return story.to_dict()
