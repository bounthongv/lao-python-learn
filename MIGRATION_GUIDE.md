#!/usr/bin/env python3
"""
Guide to run database migration on Render PostgreSQL
"""

print("=" * 70)
print("DATABASE MIGRATION GUIDE FOR RENDER POSTGRESQL")
print("=" * 70)

print("""
You have 2 SQL migration files in your project:
  1. init_db.sql (10,061 bytes) - Initial schema + 5 Lao lessons
  2. migrate_multilingual.sql (1,097 bytes) - Add lang column support

Since your app is already deployed but likely has NO lessons (empty),
you should run BOTH migrations.

═══════════════════════════════════════════════════════════════════════
METHOD 1: Using Render's Web Console (Easiest)
═══════════════════════════════════════════════════════════════════════

Step 1: Get Database Connection
-------------------------------
1. Go to Render Dashboard: https://dashboard.render.com
2. Click on your PostgreSQL database service
3. Go to "Connect" tab
4. Copy the "Connection String" (looks like: postgresql://user:pass@host:5432/db)
5. Keep this tab open

Step 2: Run Migration via Shell
-------------------------------
1. Go back to your WEB SERVICE (lao-python-learn)
2. Click on "Shell" tab
3. Run the following commands:

   # First, run the initial schema + lessons
   cat /opt/render/project/src/init_db.sql | psql "$DATABASE_URL"
   
   # Then, run the multilingual migration
   cat /opt/render/project/src/migrate_multilingual.sql | psql "$DATABASE_URL"

Step 3: Verify
--------------
Run this to check if lessons are loaded:
   psql "$DATABASE_URL" -c "SELECT id, title, lang FROM lessons ORDER BY \"order\";"

Expected output:
   id | title                    | lang
   ----+--------------------------+------
    1 | 1. ພື້ນຖານ Python        | lo
    2 | 2. ໃຊ້ງານເງື່ອນໄຂ        | lo
    3 | 3. ລູກສອນ                 | lo
    4 | 4. ລິສັດ                   | lo
    5 | 5. ຟັງຊັນ                 | lo
   (5 rows)

═══════════════════════════════════════════════════════════════════════
METHOD 2: Using Local psql (If you have PostgreSQL installed)
═══════════════════════════════════════════════════════════════════════

Step 1: Install PostgreSQL client (if not already installed)
-------------------------------------------------------------
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install libpq

Step 2: Connect to Render Database
-----------------------------------
psql "postgresql://USER:PASSWORD@HOST:PORT/DATABASE"

Replace with actual values from your Render connection string.

Step 3: Run migrations
-----------------------
# Copy the SQL file content and paste into psql, OR:

psql "postgresql://USER:PASSWORD@HOST:PORT/DATABASE" -f init_db.sql
psql "postgresql://USER:PASSWORD@HOST:PORT/DATABASE" -f migrate_multilingual.sql

═══════════════════════════════════════════════════════════════════════
METHOD 3: Using pgAdmin or DBeaver (GUI Tools)
═══════════════════════════════════════════════════════════════════════

1. Open pgAdmin/DBeaver
2. Connect using Render's connection string
3. Open SQL editor
4. Copy-paste content from init_db.sql and run
5. Copy-paste content from migrate_multilingual.sql and run

═══════════════════════════════════════════════════════════════════════
WHAT THE MIGRATIONS DO
═══════════════════════════════════════════════════════════════════════

init_db.sql:
  ✓ Creates 'lessons' table with columns: id, title, slug, content_markdown,
    example_code, "order", created_at
  ✓ Inserts 5 Lao-language Python lessons
  ✓ Sets default lang='lo' for all lessons

migrate_multilingual.sql:
  ✓ Adds 'lang' column to lessons table (if not exists)
  ✓ Creates 'ui_translations' table for future UI text translations
  ✓ Updates existing lessons to have lang='lo'
  ✓ Creates index on (lang, "order") for faster queries

═══════════════════════════════════════════════════════════════════════
AFTER MIGRATION
═══════════════════════════════════════════════════════════════════════

1. Redeploy the web service (Manual Deploy)
2. Visit: https://lao-python-learn.onrender.com
3. You should see:
   - Language selector dropdown (🇱🇦 🇺🇸 🇹🇭 🇨🇳)
   - 5 lessons in Lao language
   - Code playground with examples

═══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════

Q: "relation 'lessons' does not exist"
A: Run init_db.sql first (creates the table)

Q: "column 'lang' does not exist"
A: Run migrate_multilingual.sql (adds the lang column)

Q: "connection refused"
A: Check that your PostgreSQL service is "Available" (green status)

Q: Lessons show but empty
A: Check that the INSERT statements succeeded in init_db.sql

Q: Language selector not showing
A: This is a UI issue - check app.py has the language dropdown code

""")

print("=" * 70)
print("RECOMMENDED: Use METHOD 1 (Render Shell) - it's the easiest!")
print("=" * 70)
