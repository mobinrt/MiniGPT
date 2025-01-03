from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ALTER COLUMN "title" TYPE VARCHAR(15) USING "title"::VARCHAR(15);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ALTER COLUMN "title" TYPE VARCHAR(50) USING "title"::VARCHAR(50);"""
