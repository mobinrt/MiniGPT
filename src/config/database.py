from tortoise import Tortoise

from . import TORTOISE_ORM


class Database:
    def __init__(self):
        self.db_config = TORTOISE_ORM

    async def init_db(self):
        await Tortoise.init(self.db_config)
        await Tortoise.generate_schemas()


db = Database()
