from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_links_user_id_9be767";
        CREATE INDEX "idx_links_user_id_ab66e3" ON "links" ("user_id", "project_id", "chat_id", "link_url");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_links_user_id_ab66e3";
        CREATE INDEX "idx_links_user_id_9be767" ON "links" ("user_id", "project_id", "chat_id");"""
