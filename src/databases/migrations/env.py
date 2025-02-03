from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401
from alembic import context
from sqlalchemy import engine_from_config, pool

from configs.config import db_settings
from models import *  # noqa: F403
from models.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    postgres_server = db_settings.POSTGRES_HOST
    postgres_user = db_settings.POSTGRES_USER
    postgres_password = db_settings.POSTGRES_PASSWORD
    postgres_db = db_settings.POSTGRES_DB
    postgres_port = db_settings.POSTGRES_PORT

    return (
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_server}:{postgres_port}/{postgres_db}"
    )


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)

    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
