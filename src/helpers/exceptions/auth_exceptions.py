from .base_exception import BaseError


class InvalidCredentialsError(BaseError):
    def __init__(self):
        super().__init__("Incorrect name or password")


class UnAthorize(BaseError):
    def __init__(self):
        super().__init__("Not authenticated")


class AccessDenied(BaseError):
    def __init__(self):
        super().__init__("Access forbidden: insufficient role")


class InvalidTokenError(BaseError):
    def __init__(self):
        super().__init__("Invalid token")
