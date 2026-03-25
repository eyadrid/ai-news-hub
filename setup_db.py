#!/usr/bin/env python3
"""Initialize the PostgreSQL database and create tables."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def get_base_url() -> str:
    """Get connection URL without database name."""
    # Check for full DATABASE_URL first (preferred for deployment)
    if os.getenv("DATABASE_URL"):
        # Remove database name from full URL
        db_url = os.getenv("DATABASE_URL")
        return db_url.rsplit("/", 1)[0]

    # Fall back to individual components (for local development)
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}"

def get_db_url() -> str:
    """Get connection URL with database name."""
    # Check for full DATABASE_URL first (preferred for deployment)
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")

    # Fall back to individual components (for local development)
    db = os.getenv("POSTGRES_DB")
    return f"{get_base_url()}/{db}"

def create_database():
    """Create the database if it doesn't exist."""
    base_url = get_base_url()
    db_url = os.getenv("DATABASE_URL")

    # Extract database name from DATABASE_URL or env var
    if db_url:
        db_name = db_url.rsplit("/", 1)[-1]
    else:
        db_name = os.getenv("POSTGRES_DB")

    print(f"Connecting to PostgreSQL server...")
    engine = create_engine(base_url)

    try:
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            if result.fetchone():
                print(f"✓ Database '{db_name}' already exists")
                return True

            # Create database
            conn.execute(text(f"CREATE DATABASE \"{db_name}\""))
            conn.commit()
            print(f"✓ Created database '{db_name}'")
            return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False
    finally:
        engine.dispose()

def create_tables():
    """Create all tables in the database."""
    print(f"Creating tables...")
    from app.database.models import Base
    from sqlalchemy import create_engine

    engine = create_engine(get_db_url())
    try:
        Base.metadata.create_all(engine)
        print("✓ Tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("=" * 50)
    print("Database Initialization")
    print("=" * 50)

    if not create_database():
        sys.exit(1)

    if not create_tables():
        sys.exit(1)

    print("=" * 50)
    print("✓ Setup complete!")
    print("=" * 50)
