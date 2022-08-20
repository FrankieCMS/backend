import os

import alembic
from app.core.base import Base
from app.core.config import DATABASE_URL, POSTGRES_DB
from psycopg2 import DatabaseError
from sqlalchemy import create_engine, engine_from_config, pool

target_metadata = Base.metadata  # type: ignore


# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)

    # handle testing config for migrations
    if os.environ.get("TESTING"):
        # connect to primary db
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        # drop testing db is exists and create a fresh one
        with default_engine.connect() as default_conn:
            CLOSE_CONNECTION_SQL = f"SELECT pg_terminate_backend(pg_stat_activity.pid)\
            FROM pg_stat_activity WHERE pg_stat_activity.datname = '{POSTGRES_DB}_test'\
            AND pid <> pg_backend_pid();"

            default_conn.execute(CLOSE_CONNECTION_SQL)
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}_test")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError(
            "Running testing migrations offline currently not permitted."
        )
    alembic.context.configure(url=str(DATABASE_URL))
    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
