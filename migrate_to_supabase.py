#!/usr/bin/env python3
"""
Supabase Database Migration for Lao Python Learning Platform
Run this from your Linux Mint machine after creating a Supabase project.
"""

import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load Supabase connection string from environment or prompt
SUPABASE_URL: str = os.environ.get("SUPABASE_DB_URL", "").strip()

if not SUPABASE_URL:
    print("❌ SUPABASE_DB_URL environment variable not set")
    print(
        "PowerShell: $env:SUPABASE_DB_URL='postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres'"
    )
    print(
        "Bash:       export SUPABASE_DB_URL='postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres'"
    )
    print(
        "Get this from Supabase Dashboard > Settings > Database > Connection string > Transaction pooler"
    )
    sys.exit(1)


def get_connection():
    """Create connection to Supabase PostgreSQL"""
    try:
        # Supabase URLs use postgresql:// scheme
        if SUPABASE_URL.startswith("postgresql://"):
            return psycopg2.connect(SUPABASE_URL, cursor_factory=RealDictCursor)
        elif SUPABASE_URL.startswith("postgres://"):
            # Convert postgres:// to postgresql:// for psycopg2
            url = SUPABASE_URL.replace("postgres://", "postgresql://", 1)
            return psycopg2.connect(url, cursor_factory=RealDictCursor)
        else:
            raise ValueError(
                "Connection string must start with postgresql:// or postgres://"
            )
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)


def run_sql_file(conn, filepath, description):
    """Execute SQL file"""
    print(f"\n📄 Running: {description}")
    print(f"   File: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()

    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        print(f"   ✅ Success!")
    except Exception as e:
        conn.rollback()
        print(f"   ❌ Error: {e}")
        return False
    return True


def verify_migration(conn):
    """Verify lessons were loaded"""
    print("\n🔍 Verifying migration...")
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, title, lang FROM lessons ORDER BY "order"')
        rows = cur.fetchall()
        cur.close()

        if not rows:
            print("   ⚠️  No lessons found!")
            return False

        print(f"   Found {len(rows)} lessons:")
        for row in rows:
            print(f"     {row['id']}. {row['title']} (lang: {row['lang']})")
        return True
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False


def main():
    print("=" * 60)
    print("SUPABASE DATABASE MIGRATION")
    print("Lao Python Learning Platform")
    print("=" * 60)

    # Get project directory (works on Windows and Linux)
    project_dir = Path(__file__).resolve().parent

    # Check SQL files exist
    init_sql = project_dir / "init_db.sql"
    multi_sql = project_dir / "migrate_multilingual.sql"

    for f in [init_sql, multi_sql]:
        if not f.exists():
            print(f"❌ Missing: {f}")
            sys.exit(1)

    # Connect to Supabase
    print(f"\n🔌 Connecting to Supabase...")
    conn = get_connection()
    print("   ✅ Connected!")

    # Run migrations
    success = True
    success &= run_sql_file(conn, init_sql, "Initial schema + 5 Lao lessons")
    success &= run_sql_file(
        conn, multi_sql, "Multilingual support (lang column + index)"
    )

    # Verify
    if success:
        success &= verify_migration(conn)

    conn.close()

    print("\n" + "=" * 60)
    if success:
        print("✅ MIGRATION COMPLETE!")
        print("\nNext steps:")
        print("1. Copy your Supabase connection string")
        print("2. Go to Render Dashboard > your web service > Environment")
        print("3. Add: DATABASE_URL = your_supabase_connection_string")
        print("4. Trigger Manual Deploy on Render")
    else:
        print("❌ MIGRATION FAILED - check errors above")
    print("=" * 60)


if __name__ == "__main__":
    main()
