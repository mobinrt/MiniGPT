from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "projects" ALTER COLUMN "name" TYPE VARCHAR(15) USING "name"::VARCHAR(15);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "projects" ALTER COLUMN "name" TYPE VARCHAR(50) USING "name"::VARCHAR(50);"""
