from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from alembic.config import Config
from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from orderful.core.settings import settings
from orderful.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def skip_empty_migration(
        config: Config, script: MigrationScript, directives: list[MigrationScript]
    ) -> None:
        if config.cmd_opts.autogenerate and script.upgrade_ops.is_empty():
            directives[:] = []

    def enumerate_migration_name(script: MigrationScript) -> None:
        head = ScriptDirectory.from_config(context.config).get_current_head()

        if head is None:
            current_revision_id = 1
        else:
            previous_revision_id = int(head[:4].strip("0"))
            current_revision_id = previous_revision_id + 1

        script.rev_id = f"{current_revision_id:04}_{script.rev_id}"

    def process_revision_directives(
        context: MigrationContext, revision: tuple, directives: list[MigrationScript]
    ) -> None:
        script = directives[0]

        skip_empty_migration(context.config, script, directives)
        enumerate_migration_name(script)

    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
