# -*- coding: utf-8 -*-
import json

from functions.mutations import (
    add_nest_user,
    add_story_attachment,
    create_nest,
    create_story
)
from functions.queries import (
    get_nest,
    get_nests,
    get_story,
    get_stories
)


def main(event, context):
    """
    Handler function for graphql functions
    """
    print(json.dumps(event))

    # Add any new mutation or query definitions to this dictionary
    # and set it to the function that processes that action.
    actions = {
        "Mutation": {
            "createNest": create_nest,
            "addNestUser": add_nest_user,
            "createStory": create_story,
            "addStoryAttachment": add_story_attachment
        },
        "Query": {
            "nest": get_nest,
            "nests": get_nests,
            "story": get_story,
            "stories": get_stories
        }
    }

    # extract information as to which query or mutation is being requested
    field_name = event["info"]["fieldName"]
    parent_type_name = event["info"]["parentTypeName"]

    # TODO: Add error handling if the action does not exist
    handler_function = actions[parent_type_name][field_name]

    # invoke the proper function
    return handler_function(event)
