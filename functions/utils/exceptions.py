# -*- coding: utf-8 -*-

class BaseExceptionResponse(Exception):
    def __init__(self, message: str = None):
        self._message = message
        self.resp = None

    def __str__(self):
        return self.response

    def __repr__(self):
        return self.response

    @property
    def json(self):
        return self.resp or self._message

    @property
    def response(self):
        return self.json


class UnauthorizedException(BaseExceptionResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resp = "Unauthorized"
