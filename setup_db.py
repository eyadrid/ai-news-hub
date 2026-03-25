#!/usr/bin/env python3
"""
One-time setup script to initialize database tables.
Run this after setting up Railway PostgreSQL.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    from app.database.create_tables import create_all

    print("🔧 Initializing database tables...")
    create_all()
    print("✅ Database tables created successfully!")

except Exception as e:
    print(f"❌ Error creating tables: {e}")
    print("\nTroubleshooting:")
    print("- Check all POSTGRES_* environment variables are set")
    print("- Verify PostgreSQL database is running")
    print("- Ensure database credentials are correct")
    sys.exit(1)
