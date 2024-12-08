import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from database.models import Base
from core.settings import DATABASE_URL
import re

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def clean_database_url(url):
    # Convert asyncpg to psycopg2 for migrations
    url = url.replace("postgresql+asyncpg://", "postgresql://")
    url = re.sub(r"\?ssl=require", "", url)
    return url


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    sync_url = clean_database_url(DATABASE_URL)
    configuration["sqlalchemy.url"] = sync_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={
            "sslmode": "require"} if "amazonaws.com" in DATABASE_URL else {}
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


def run_migrations_offline():
    sync_url = clean_database_url(DATABASE_URL)
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
