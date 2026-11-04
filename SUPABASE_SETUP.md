# Supabase Setup Guide for Lao Python Learning Platform

## Step 1: Create Supabase Project

1. Go to https://supabase.com and sign in (or create account)
2. Click **"New Project"**
3. Fill in:
   - **Name**: `lao-python-learn` (or your choice)
   - **Database Password**: Generate a strong password — **save this!**
   - **Region**: Choose closest to Laos (e.g., Singapore `ap-southeast-1`)
4. Click **"Create new project"** — takes ~2 minutes

## Step 2: Get Connection String

1. In your Supabase project, go to **Settings** (gear icon) → **Database**
2. Scroll to **Connection string** → **Transaction pooler** (recommended for external connections)
3. Copy the connection string — it looks like:
   ```
   postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:6543/postgres
   ```
   **Important**: Replace `[YOUR-PASSWORD]` with the password you set in Step 1.

## Step 3: Run Migration from Your Windows Machine

Open PowerShell in the project folder:

```powershell
# Navigate to project
cd D:\lao-python-learn

# Set the connection string (replace with YOUR actual string)
$env:SUPABASE_DB_URL='postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres'

# Use the project Python 3.12 interpreter
py -3.12 migrate_to_supabase.py
```

> Use the **Direct connection** (port 5432) or **Session pooler** for the one-time
> migration. The **Transaction pooler** (port 6543) is fine for the running app.

**Expected output:**
```
============================================================
SUPABASE DATABASE MIGRATION
Lao Python Learning Platform
============================================================

🔌 Connecting to Supabase...
   ✅ Connected!

📄 Running: Initial schema + 5 Lao lessons
   File: D:\lao-python-learn\init_db.sql
   ✅ Success!

📄 Running: Multilingual support (lang column + index)
   File: D:\lao-python-learn\migrate_multilingual.sql
   ✅ Success!

🔍 Verifying migration...
   Found 5 lessons:
     1. 1. ພື້ນຖານ Python (lang: lo)
     2. 2. ເງື່ອນໄຂ (lang: lo)
     3. 3. ລູກສອນ (lang: lo)
     4. 4. ລິສັດ (lang: lo)
     5. 5. ຟັງຊັນ (lang: lo)

============================================================
✅ MIGRATION COMPLETE!

Next steps:
1. Copy your Supabase connection string
2. Go to Render Dashboard > your web service > Environment
3. Add: DATABASE_URL = your_supabase_connection_string
4. Trigger Manual Deploy on Render
============================================================
```

## Step 4: Configure Render Web Service

1. Go to https://dashboard.render.com
2. Click on your **lao-python-learn** web service
3. Go to **Environment** tab
4. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: (your Supabase connection string from Step 2)
5. Click **Save Changes**

## Step 5: Deploy

1. Still in Render dashboard, go to **Manual Deploy** → **Deploy latest commit**
2. Wait for build to complete
3. Visit: https://lao-python-learn.onrender.com

## Supabase Free Tier Limits

| Resource | Limit |
|----------|-------|
| Database size | 500 MB |
| Bandwidth | 2 GB/month |
| Projects | Unlimited |
| API requests | Unlimited |

**Your use case** (5 lessons + minimal traffic) is well within free limits.

## Troubleshooting

### "connection refused" or timeout
- Make sure you're using the **Transaction pooler** string (port 6543), not Session pooler (port 5432)
- Check Supabase project is not paused (free projects pause after 1 week inactivity)

### "password authentication failed"
- The password in the connection string must match what you set during project creation
- Regenerate password in Supabase Settings → Database if needed

### Migration says "relation already exists"
- This is fine — the SQL uses `IF NOT EXISTS` and `IF NOT EXISTS` for index
- Just means you ran it before

### Render shows "Database error" in logs
- Verify `DATABASE_URL` is set correctly in Render Environment
- Check the connection string has no extra spaces or quotes
- Supabase requires SSL — the connection string should work as-is

## Useful Supabase Dashboard Links

- **SQL Editor**: Run ad-hoc queries
- **Table Editor**: View/edit data visually
- **Logs**: Check query performance
- **Backups**: Automatic daily backups (7-day retention on free tier)