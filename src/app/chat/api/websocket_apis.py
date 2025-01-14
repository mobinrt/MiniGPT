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
from huggingface_hub import InferenceClient
from datetime import datetime

from src.config.redis import redis_client
from src.config.settings import Settings
from src.helpers.enum.message_status import MessageStatus
from src.app.chat.model import ChatModel
from src.app.chat.model import ResponceModel, PromptModel, WebSocketSession
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.exceptions.base_exception import BaseError

from src.helpers.auth.dependencies import get_auth_controller
from src.helpers.auth.controller import AuthController

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
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


GUEST_MESSAGE_LIMIT = 5


@router.websocket("/guest/")
async def guest_websocket(websocket: WebSocket, guest_id: str = Query(...)):
    await websocket.accept()
    print("aaaaaaaa")
    try:
        message_count_key = f"guest:{guest_id}:message_count"
        if not await redis_client.exists(message_count_key):
            await redis_client.set(message_count_key, 0, ex=3600)

        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "").strip()
            if not user_message:
                continue

            current_count = int(await redis_client.get(message_count_key))
            if current_count >= GUEST_MESSAGE_LIMIT:
                await websocket.send_json(
                    {"error": "Message limit reached. Please sign up to continue."}
                )
                await websocket.close()
                break

            ai_response = (
                client.chat.completions.create(
                    model="Qwen/Qwen2.5-72B-Instruct",
                    messages=[{"role": "user", "content": user_message}],
                    max_tokens=200,
                )
                .choices[0]
                .message.content
            )
            print("ai_response: ", ai_response)

            await redis_client.incr(message_count_key)

            await websocket.send_json({"response": ai_response})

    except WebSocketDisconnect:
        print(f"Guest {guest_id} disconnected")
    except Exception as e:
        await websocket.close()
        print(f"WebSocket error: {str(e)}")


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
        print(f"User {current_user.username} disconnected")

    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    finally:
        if session:
            async with in_transaction():
                session.disconnected_at = datetime.now()
                await session.save()
