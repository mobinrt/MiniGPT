from .settings import settings

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
                'src.app.chat.model.websocket_model',
                'aerich.models' 
            ],
            'default_connection': 'default'
        },
    },
}
