from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(200) NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_premium" BOOL NOT NULL  DEFAULT False,
    "pic_url" VARCHAR(255)
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE TABLE IF NOT EXISTS "projects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(100) NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "chats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(50) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "project_id" INT NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_chats_project_36ceb2" ON "chats" ("project_id");
CREATE TABLE IF NOT EXISTS "prompts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "content" TEXT NOT NULL,
    "status" VARCHAR(1) NOT NULL  DEFAULT 'S',
    "chat_id" INT NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_prompts_chat_id_35ae38" ON "prompts" ("chat_id");
COMMENT ON COLUMN "prompts"."status" IS 'SENT: S\nDELIVERED: D\nREAD: R\nFAILED: F';
CREATE TABLE IF NOT EXISTS "responces" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "content" TEXT NOT NULL,
    "status" VARCHAR(1) NOT NULL  DEFAULT 'S',
    "like_status" VARCHAR(1) NOT NULL  DEFAULT 'N',
    "chat_id" INT NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_responces_prompt__24f884" ON "responces" ("prompt_id");
COMMENT ON COLUMN "responces"."status" IS 'SENT: S\nDELIVERED: D\nREAD: R\nFAILED: F';
COMMENT ON COLUMN "responces"."like_status" IS 'LIKE: L\nDISLIKE: D\nNONE: N';
CREATE TABLE IF NOT EXISTS "links" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "link_url" VARCHAR(255),
    "is_public" BOOL NOT NULL  DEFAULT False,
    "chat_id" INT REFERENCES "chats" ("id") ON DELETE CASCADE,
    "project_id" INT REFERENCES "projects" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_links_user_id_9be767" ON "links" ("user_id", "project_id", "chat_id");
CREATE TABLE IF NOT EXISTS "websocket_sessions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "connected_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "disconnected_at" TIMESTAMPTZ,
    "chat_id" INT NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_websocket_s_user_id_6e88d5" ON "websocket_sessions" ("user_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
