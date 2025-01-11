from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ADD "dummy_field" VARCHAR(50);
        ALTER TABLE "prompts" ADD "dummy_field" VARCHAR(50);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" DROP COLUMN "dummy_field";
        ALTER TABLE "prompts" DROP COLUMN "dummy_field";"""
