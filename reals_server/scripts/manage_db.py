import click
from sqlalchemy import create_engine, MetaData, inspect
from app.utils.migration_generator import MigrationGenerator
from app.models import BaseModel
from app.core.config import settings


@click.group()
def cli():
    """Database management commands"""
    pass


@cli.command()
@click.option("--message", "-m", required=True, help="Migration message")
def makemigrations(message):
    """Generate database migrations"""
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)

    with engine.connect() as conn:
        generator = MigrationGenerator(BaseModel.metadata, inspector, conn)
        filepath = generator.generate_migration(message)
        click.echo(f"Generated migration: {filepath}")


@cli.command()
def migrate():
    """Apply migrations"""
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    click.echo("Applied migrations successfully")


if __name__ == "__main__":
    cli()
