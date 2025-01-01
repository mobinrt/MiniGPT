class BaseError(Exception):
    def __init__(self, message: str = "Server Internal Error"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
