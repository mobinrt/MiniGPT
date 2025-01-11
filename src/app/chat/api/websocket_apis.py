from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    HTTPException,
    status,
    Query,
)
from tortoise.transactions import in_transaction
from tortoise.exceptions import DoesNotExist
from huggingface_hub import InferenceClient
from datetime import datetime

from src.helpers.auth import oauth2_scheme
from src.config.settings import Settings
from src.helpers.enum.message_status import MessageStatus
from src.app.user.model import UserModel
from src.app.chat.model import ChatModel
from src.app.chat.model import ResponceModel, PromptModel, WebSocketSession
from src.helpers.auth.dependencies import get_current_user
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.exceptions.base_exception import BaseError

from src.helpers.auth.dependencies import get_auth_controller
from src.helpers.auth.controller import AuthController

router = APIRouter(
    prefix="/websocket",
    tags=["websocket"],
)


client = InferenceClient(api_key=Settings.api_key)


@router.get("/docs")
async def docs_info():
    """
    WebSocket Documentation:
    Connect to the WebSocket at `/websocket/{chat_id}/`. Send JSON messages with the following format:
    - `{ "message": "Your message here" }`
    The server will respond with JSON containing the AI-generated response.

    Example WebSocket Workflow:
    1. Connect to the WebSocket endpoint.
    2. Send a message as JSON.
    3. Receive the response as JSON.
    """
    return {"info": "WebSocket API documentation"}


@router.websocket("/{chat_id}/")
async def chat_websocket(
    websocket: WebSocket,
    chat_id: int,
    token: str = Query(...),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    await websocket.accept()
    session = None
    try:
        current_user = await auth_controller.get_current_user(token)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token is missing"
            )

        async with in_transaction():
            chat = await ChatModel.get(id=chat_id).first()
            if not chat:
                raise NotFoundError()

            session = await WebSocketSession.create(
                user=current_user, chat=chat, connected_at=datetime.now()
            )

            while True:
                data = await websocket.receive_json()

                user_message = data.get("message", "").strip()
                if not user_message:
                    continue

                project = await chat.project
                project_name = project.name
                if project_name:
                    message_text = f"{project_name}: {user_message}"
                    print(message_text)
                else:
                    message_text = f"{user_message}"
                    print(message_text)

                prompt = await PromptModel.create(
                    chat=chat, content=message_text, status=MessageStatus.SENT.value
                )

                try:
                    ai_response = (
                        client.chat.completions.create(
                            model="Qwen/Qwen2.5-72B-Instruct",
                            messages=[{"role": "user", "content": message_text}],
                            max_tokens=200,
                        )
                        .choices[0]
                        .message.content
                    )
                    print("ai_response: ", ai_response)
                except Exception as e:
                    return str(e)

                await ResponceModel.create(
                    prompt=prompt,
                    content=ai_response,
                    status=MessageStatus.DELIVERED.value,
                    chat=chat,
                )

                await websocket.send_json(
                    {"prompt_id": prompt.id, "response": ai_response}
                )

    except WebSocketDisconnect:
        if session:
            async with in_transaction():
                session.disconnected_at = datetime.now()
                await session.save()
        print(f"User {current_user.username} disconnected")

    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
