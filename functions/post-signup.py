# -*- coding: utf-8 -*-
from functions.utils.models import Nest


def add_usernames_to_nests(event, context):
    """
    Once the users are created, we need to check if the
    email address is stored in any nests.
    If the email is part of the nest, we must add the
    corrisponding username
    """
    print(event)
    email = event["request"]["userAttributes"]["email"]
    username = event["userName"]

    # now we query all nests
    nests = Nest.scan(Nest.nestComponent == 'NEST')

    # I am aware that is a super ugly for loop and I don't care
    for nest in nests:
        for user in nest.users:
            if user["email"] == email:
                user["username"] = username
                nest.save()

    return event
