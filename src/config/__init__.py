from .settings import settings

TORTOISE_ORM = {
    'connections': {'default': settings.database_url},
    'apps': {
        'models': {
            'models': [
                'src.app.user.model',
                'src.app.project.model',
                'src.app.chat.model',
                'src.app.chat.message.model',
                'src.app.share_link.model',
                'src.helpers.websocket.model',
                'aerich.models' 
            ],
            'default_connection': 'default'
        },
    },
}
