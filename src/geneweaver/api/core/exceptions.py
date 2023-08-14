""""""
from fastapi import HTTPException


class Auth0UnauthenticatedException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(401, **kwargs)


class Auth0UnauthorizedException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(403, **kwargs)


class NotAHeaderRowError(Exception):
    pass


class InvalidBatchValueLine(Exception):
    pass


class MultiLineStringError(Exception):
    pass


class IgnoreLineError(Exception):
    pass


class MissingRequiredHeaderError(Exception):
    pass


class InvalidScoreThresholdException(Exception):
    pass
