# -*- coding: utf-8 -*-
from functions.utils.exceptions import UnauthorizedException
from functions.utils.models import Nest


def requires_nest_access(function):
    def wrapper_function(*args, **kwargs):
        nestId = args[0]["arguments"].get("nestId")
        user = (args[0]["identity"] or {}).get("username")

        # check if user is in nest users or is the nest owner
        try:
            nest = Nest.get(nestId, 'NEST')
        except Nest.DoesNotExist:
            raise UnauthorizedException()

        if user not in [*nest.users, nest.owner]:
            raise UnauthorizedException()

        return function(*args, **kwargs)

    return wrapper_function


def requires_nest_ownership(function):
    def wrapper_function(*args, **kwargs):
        nestId = args[0]["arguments"].get("nestId")
        user = (args[0]["identity"] or {}).get("username")

        # check if user is in nest users or is the nest owner
        try:
            nest = Nest.get(nestId, 'NEST')
        except Nest.DoesNotExist:
            raise UnauthorizedException()

        if user != nest.owner:
            raise UnauthorizedException()

        return function(*args, **kwargs)

    return wrapper_function
