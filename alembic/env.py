import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add your project's root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your models and Base
from models.user import User
from models.product import Product
from models.pricing import Pricing
from models import Base  # Make sure Base is imported

# Alembic Config object
config = context.config

# Set target_metadata to your Base.metadata
target_metadata = Base.metadata  # Base is where the metadata for all models is collected
target_metadata = User.metadata  # Base is where the metadata for all models is collected
target_metadata = Product.metadata  # Base is where the metadata for all models is collected
target_metadata = Pricing.metadata  # Base is where the metadata for all models is collected

# Other configurations in env.py...

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Connect to the engine and run migrations
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
