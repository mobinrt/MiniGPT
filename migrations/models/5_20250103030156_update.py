from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP CONSTRAINT "fk_users_projects_d4663be4";
        CREATE UNIQUE INDEX "uid_users_active__307e84" ON "users" ("active_project_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_users_active__307e84";
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_projects_d4663be4" FOREIGN KEY ("active_project_id") REFERENCES "projects" ("id") ON DELETE SET NULL;"""
