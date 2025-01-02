from .base_exception import BaseError


class UserNotFoundError(BaseError):
    def __init__(self):
        super().__init__("User not found")


class DeleteAdmin(BaseError):
    def __init__(self):
        super().__init__("Admin can not be deleted under any circumstances")
