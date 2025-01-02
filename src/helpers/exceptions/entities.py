from .base_exception import BaseError


class NotFoundError(BaseError):
    def __init__(self):
        super().__init__("Entity not found")


class DeleteAdmin(BaseError):
    def __init__(self):
        super().__init__("Admin can not be deleted under any circumstances")
