from .message_schema import MessageBase, MessageDisplay


class ResponceCreate(MessageBase):
    prompt_id: int


class ResponceDisplay(MessageDisplay):
    prompt_id: int
    like_status: str
