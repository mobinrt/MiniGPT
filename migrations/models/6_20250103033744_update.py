from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_users_active__307e84";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_users_active__307e84" ON "users" ("active_project_id");"""
