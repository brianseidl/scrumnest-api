# -*- coding: utf-8 -*-
from functions.utils.auth import requires_nest_access
from functions.utils.models import Nest, Story


@requires_nest_access
def get_nest(event):
    try:
        nest = Nest.get(event['arguments']['nestId'], 'NEST')
    except Nest.DoesNotExist:
        return None

    return nest.to_dict()


def get_nests(event):
    return [nest.to_dict() for nest in Nest.scan(Nest.nestComponent == 'NEST')]


@requires_nest_access
def get_story(event):
    try:
        story = Story.get(event["arguments"]["nestId"], f"STORY.{event['arguments']['storyId']}")
    except Story.DoesNotExist:
        return None

    return story.to_dict()


@requires_nest_access
def get_stories(event):
    stories = Story.query(event["arguments"]["nestId"], Story.nestComponent.startswith('STORY'))
    return [story.to_dict() for story in stories]
