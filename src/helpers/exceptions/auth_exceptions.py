from .base_exception import BaseError


class InvalidCredentialsError(BaseError):
    message = "Incorrect name or password"


class UnAthorize(BaseError):
    message = "Not authenticated"


class AccessDenied(BaseError):
    message = "Access forbidden: insufficient role"
