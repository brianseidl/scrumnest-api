# -*- coding: utf-8 -*-
import ulid
import boto3
from datetime import datetime
import dateutil.tz

from functions.utils.auth import requires_nest_access, requires_nest_ownership
from functions.utils.common import get_user_by_email, FROM_EMAIL
from functions.utils.models import Nest, Story, Attachment, Comment

ses = boto3.client("ses")


def create_nest(event):
    """
    createNest function to create a nest object in the dynamodb table
    """
    username = (event["identity"] or {}).get("username")

    nest = Nest(
        str(ulid.new().int >> 64),
        'NEST',
        name=event["arguments"].get("name", ""),
        owner=username
    )
    nest.save()

    return nest.to_dict()


@requires_nest_ownership
def add_nest_user(event):
    sender_username = (event["identity"] or {}).get("username")
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')
    users = list(nest.users)
    email = event["arguments"]["email"]

    user_obj = {
        "email": email,
        "username": get_user_by_email(event["arguments"]["email"]) or ""
    }

    users.append(user_obj)
    # make unique
    users = list({v['email']: v for v in users}.values())
    nest.users = users
    nest.save()

    # send email
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': f"You are invited to join the nest: {nest.name}"},
            'Body': {
                'Text': {'Data': f"Hi there,\n\nYou have been added to {nest.name} by {sender_username}.\nCheck it out at https://scrumnest.com/nests/{nest.nestId}"}
            }
        }
    )

    return nest.to_dict()


@requires_nest_ownership
def remove_nest_user(event):
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')
    users = list(nest.users)
    email = event["arguments"]["email"]

    for i, user in enumerate(users):
        if user["email"] == email:
            users.pop(i)

    nest.users = users
    nest.save()

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

    return nest.to_dict(sprint=event['arguments'].get('sprint'))  # Return Nest for UI simplification


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
def delete_story_attachment(event):
    # get story so we know it exists first
    story = Story.get(event["arguments"]["nestId"], f"STORY.{event['arguments']['storyId']}")
    attachment_key = event["arguments"]["key"]

    attachments = story.attachments

    for i, attachment in enumerate(attachments):
        if attachment["key"] == attachment_key:
            attachments.pop(i)
            break

    story.attachments = attachments
    story.save()

    return story.to_dict()


@requires_nest_access
def add_comment(event):
    # get story so we know it exists first
    story = Story.get(event["arguments"]["nestId"], f"STORY.{event['arguments']['storyId']}")

    comment_data = event["arguments"].pop('comment')

    comment = Comment(
        username=(event["identity"] or {}).get("username", ""),
        content=comment_data,
        createdAt=datetime.now().replace(tzinfo=dateutil.tz.gettz()),
    )

    story.comments.insert(0, comment)
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
            content=event["arguments"].pop('comment'),
            createdAt=datetime.now().replace(tzinfo=dateutil.tz.gettz()),
        )
        story.comments.insert(0, comment)

    dateToBeCompleted = event["arguments"].get("dateToBeCompleted")

    # Parse string to datetime obj
    if dateToBeCompleted:
        event["arguments"]["dateToBeCompleted"] = datetime.strptime(dateToBeCompleted, '%Y-%m-%d')

    # Set parameters
    for arg, value in event["arguments"].items():
        if value:
            setattr(story, arg, value)

    story.save()

    return Nest.get(nest_id, "NEST").to_dict(sprint=event['arguments'].get('sprint'))  # Return Nest for UI simplification


@requires_nest_access
def delete_story(event):
    nest_id = event["arguments"].pop('nestId')
    story_id = event["arguments"].pop('storyId')

    story = Story.get(nest_id, f"STORY.{story_id}")
    story.delete()

    return Nest.get(nest_id, "NEST").to_dict(sprint=event['arguments'].get('sprint'))  # Return Nest for UI simplification


@requires_nest_access
def add_sprint(event):
    nest = Nest.get(event["arguments"]["nestId"], 'NEST')
    nest.sprints += 1
    nest.save()

    return nest.to_dict()
