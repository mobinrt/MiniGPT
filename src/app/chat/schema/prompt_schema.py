from .message_schema import MessageBase, MessageDisplay


class PromptCreate(MessageBase):
    chat_id: int


class PromptUpdate(MessageBase):
    pass


class PromptDisplay(MessageDisplay):
    pass
