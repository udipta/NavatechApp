from alembic import command
from alembic.config import Config


def run_migrations(connection_url=None):
    alembic_cfg = Config("alembic.ini")
    if connection_url:
        alembic_cfg.set_main_option("sqlalchemy.url", connection_url)
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_migrations()
