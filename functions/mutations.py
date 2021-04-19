# -*- coding: utf-8 -*-
import ulid
import boto3

from functions.utils.auth import requires_nest_access, requires_nest_ownership
from functions.utils.common import get_user_by_email, FROM_EMAIL
from functions.utils.models import Nest, Story, Attachment, Comment

ses = boto3.client("ses")


def create_nest(event):
    """
    createNest function to create a nest object in the dynamodb table
    """
    nest = Nest(
        ulid.new().int >> 64,
        'NEST',
        name=event["arguments"].get("name", ""),
        owner=(event["identity"] or {}).get("username")
    )
    nest.save()

    return nest.to_dict()


@requires_nest_ownership
def add_nest_user(event):
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')
    users = list(nest.users)
    email = event["arguments"]["email"]

    user_obj = {
        "email": email,
        "username": get_user_by_email(event["arguments"]["email"])
    }

    users.append(user_obj)
    nest.users = users
    nest.save()

    # send email
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': f"You are invited to join the nest: {nest.name}"},
            'Body': {
                'Text': {'Data': f"Hi there,\n\nYou have been added to {nest.name}.\nCheck it out at https://scrumnest.com/nests/{nest.nestId}"}
            }
        }
    )

    return nest.to_dict()


@requires_nest_access
def create_story(event):
    # get nest so we know it exists first
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')

    story = Story(
        event["arguments"]["nestId"],
        f'STORY.{ulid.new().int >> 64}',
        title=event["arguments"]["title"],
        description=event["arguments"].get("descritpion"),
        owner=event["arguments"].get("owner") or (event["identity"] or {}).get("username"),
        status=event["arguments"].get("status", "TODO") or "TODO"
    )
    story.save()

    return nest.to_dict()  # Return Nest for UI simplification


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


@requires_nest_access
def update_story(event):
    nest_id = event["arguments"].pop('nestId')
    story_id = event["arguments"].pop('storyId')
    story = Story.get(nest_id, f"STORY.{story_id}")

    # handle comments first because they don't line up with model
    if event["arguments"].get('comment'):
        comment = Comment(
            username=(event["identity"] or {}).get("username", ""),
            content=event["arguments"].pop('comment')
        )
        story.comments.append(comment)

    # Set parameters
    for arg, value in event["arguments"].items():
        if value:
            setattr(story, arg, value)

    story.save()

    return Nest.get(nest_id, "NEST").to_dict()  # Return Nest for UI simplification
