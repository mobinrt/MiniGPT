from datetime import datetime, timedelta, timezone

from aioclock import AioClock, Every

from src.app.link.model import LinkModel
from src.app.chat.model import WebSocketSession

app = AioClock()


@app.task(trigger=Every(hours=1))
async def delete_expired_links():
    current_time = datetime.now(timezone.utc)
    deleted_count = await LinkModel.filter(
        created_at__lt=current_time - timedelta(hours=24)
    ).delete()

    print(f"Deleted {deleted_count} expired links.")


@app.task(trigger=Every(hours=1))
async def delete_expired_websocket_sessions():
    current_time = datetime.now(timezone.utc)
    deleted_count = await WebSocketSession.filter(
        disconnected_at__lt=current_time - timedelta(hours=24)
    ).delete()

    print(f"Deleted {deleted_count} expired WebSocket sessions.")
