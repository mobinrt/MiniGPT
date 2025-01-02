from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "active_project_id" INT;
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_projects_d4663be4" FOREIGN KEY ("active_project_id") REFERENCES "projects" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP CONSTRAINT "fk_users_projects_d4663be4";
        ALTER TABLE "users" DROP COLUMN "active_project_id";"""
