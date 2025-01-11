from typing import TYPE_CHECKING
from tortoise import Tortoise
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from src.app.user.model import UserModel
from src.app.project.model import ProjectModel
from src.app.link.model import LinkModel
from src.app.chat.model import ChatModel
from src.app.chat.model import PromptModel, ResponceModel
from src.helpers.websocket.model import WebSocketSession


Tortoise.init_models(
    [
        "src.app.user.model",
        "src.app.project.model",
        "src.app.chat.model",
        "src.app.chat.model.message_model",
        "src.app.link.model",
        "src.helpers.websocket.model",
    ],
    "models",
)

if TYPE_CHECKING:

    class UserCreateScheme(UserModel, PydanticModel):  # type:ignore[misc]
        pass

    class UserResponseScheme(UserModel, PydanticModel):  # type:ignore[misc]
        pass

    class ProjectCreateScheme(ProjectModel, PydanticModel):  # type:ignore[misc]
        pass

    class ProjectResponseScheme(ProjectModel, PydanticModel):  # type:ignore[misc]
        pass

    class LinkCreateScheme(LinkModel, PydanticModel):  # type:ignore[misc]
        pass

    class LinkResponseScheme(LinkModel, PydanticModel):  # type:ignore[misc]
        pass

    class ChatCreateScheme(ChatModel, PydanticModel):  # type:ignore[misc]
        pass

    class ChatResponseScheme(ChatModel, PydanticModel):  # type:ignore[misc]
        pass

    class PromptCreateScheme(PromptModel, PydanticModel):  # type:ignore[misc]
        pass

    class PromptResponseScheme(PromptModel, PydanticModel):  # type:ignore[misc]
        pass

    class ResponceCreateScheme(ResponceModel, PydanticModel):  # type:ignore[misc]
        pass

    class ResponceModelResponseScheme(ResponceModel, PydanticModel):  # type:ignore[misc]
        pass

    class SessionCreateScheme(WebSocketSession, PydanticModel):  # type:ignore[misc]
        pass

    class SessionResponseScheme(WebSocketSession, PydanticModel):  # type:ignore[misc]
        pass

else:
    UserCreateScheme = pydantic_model_creator(
        UserModel, exclude_readonly=True, name="UserCreateScheme"
    )
    ProjectCreateScheme = pydantic_model_creator(
        ProjectModel, exclude_readonly=True, name="ProjectCreateScheme"
    )
    LinkCreateScheme = pydantic_model_creator(
        LinkModel, exclude_readonly=True, name="LinkCreateScheme"
    )
    ChatCreateScheme = pydantic_model_creator(
        ChatModel, exclude_readonly=True, name="ChatCreateScheme"
    )
    PromptCreateScheme = pydantic_model_creator(
        PromptModel, exclude_readonly=True, name="PromptCreateScheme"
    )
    ResponceCreateScheme = pydantic_model_creator(
        ResponceModel, exclude_readonly=True, name="ResponceCreateScheme"
    )
    SessionCreateScheme = pydantic_model_creator(
        WebSocketSession, exclude_readonly=True, name="SessionCreateScheme"
    )

    UserResponseScheme = pydantic_model_creator(UserModel, name="UserResponseScheme")
    ProjectResponseScheme = pydantic_model_creator(
        ProjectModel, name="ProjectResponseScheme"
    )
    LinkResponseScheme = pydantic_model_creator(LinkModel, name="LinkResponseScheme")
    ChatResponseScheme = pydantic_model_creator(ChatModel, name="ChatResponseScheme")

    PromptResponseScheme = pydantic_model_creator(
        PromptModel, name="PromptResponseScheme"
    )
    ResponceResponseScheme = pydantic_model_creator(
        ResponceModel, name="ResponceResponseScheme"
    )
    SessionResponseScheme = pydantic_model_creator(
        WebSocketSession, name="SessionResponseScheme"
    )
