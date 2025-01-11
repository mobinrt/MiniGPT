from .settings import settings
from src.app.chat.model.chat_model import ChatModel
from src.app.chat.model.message_model import MessageModel

TORTOISE_ORM = {
    'connections': {'default': settings.database_url},
    'apps': {
        'models': {
            'models': [
                'src.app.user.model',
                'src.app.project.model',
                'src.app.chat.model.chat_model',
                'src.app.chat.model.message_model',
                'src.app.link.model',
                'src.helpers.websocket.model',
                'aerich.models' 
            ],
            'default_connection': 'default'
        },
    },
}
