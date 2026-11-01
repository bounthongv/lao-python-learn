# Deploy Lao Python Learning Platform to Railway

## Why Railway?
- ✅ Works in Laos (no DNS blocking like Render)
- ✅ Free $5/month credit (enough for small apps)
- ✅ Native PostgreSQL support
- ✅ Docker-based (uses your existing Dockerfile)
- ✅ Simple GitHub integration

---

## Step 1: Prepare Your Code

The following files are already ready:
- `Dockerfile` — Updated for Railway's PORT env var
- `railway.json` — Railway configuration
- `init_db.sql` — Database initialization script
- `requirements.txt` — Python dependencies
- `app.py` — Gradio app (loads lessons from PostgreSQL)

---

## Step 2: Create Railway Account & Project

1. Go to **https://railway.app**
2. Sign up with **GitHub** (easiest)
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose **`bounthongv/lao-python-learn`**

Railway will:
- Detect Dockerfile automatically
- Build the image
- Deploy on a `railway.app` subdomain

---

## Step 3: Add PostgreSQL Database

1. In your Railway project dashboard
2. Click **"+ New"** → **"Database"** → **"PostgreSQL"**
3. Railway provisions a PostgreSQL instance
4. **Copy the connection variables** (auto-injected as env vars):
   - `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

---

## Step 4: Configure Environment Variables

In your **Web Service** (not the database), go to **Variables** tab and add:

| Key | Value |
|-----|-------|
| `DB_HOST` | `${{Postgres.PGHOST}}` |
| `DB_PORT` | `${{Postgres.PGPORT}}` |
| `DB_NAME` | `${{Postgres.PGDATABASE}}` |
| `DB_USER` | `${{Postgres.PGUSER}}` |
| `DB_PASSWORD` | `${{Postgres.PGPASSWORD}}` |

> Railway's `${{Postgres.XXX}}` syntax auto-references the PostgreSQL service in the same project.

---

## Step 5: Initialize Database

Once the PostgreSQL service is running:

1. Go to PostgreSQL service → **"Connect"** → **"CLI"**
2. Copy the `psql` connection command
3. Run locally:
   ```bash
   # Replace with your actual connection string
   psql "postgresql://user:pass@host:port/db" -f init_db.sql
   ```
   
   Or use Railway's web-based query tool:
   - PostgreSQL service → **"Data"** → **"Query"**
   - Paste contents of `init_db.sql` and run

---

## Step 6: Verify Deployment

1. Wait for build to complete (green checkmark)
2. Click your web service URL (e.g., `https://lao-python-learn-xxxx.railway.app`)
3. Should see: **"ຮຽນ Python"** with 5 lessons

---

## Step 7: Custom Domain (Optional)

1. Web service → **Settings** → **Domains**
2. Add your domain (e.g., `learn.yourdomain.com`)
3. Configure DNS CNAME to Railway's provided domain

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check Dockerfile, ensure `requirements.txt` has all deps |
| App crashes | Check **Logs** tab; usually missing env vars or DB connection |
| DB connection error | Verify env vars match PostgreSQL service variables |
| Lessons not showing | Run `init_db.sql` on the PostgreSQL instance |

---

## Cost Estimate

- **Web service**: ~$1-3/month (512MB RAM, minimal CPU)
- **PostgreSQL**: ~$1-2/month (shared instance)
- **Total**: ~$2-5/month (within $5 free credit)

After free credit: ~$5/month — very affordable.

---

## Files Reference

```
/home/bounthong/elearning-python/lao-python-learn/
├── Dockerfile          # Docker image (updated for Railway PORT)
├── railway.json        # Railway config
├── init_db.sql         # Database schema + 5 lessons
├── requirements.txt    # Python deps
├── app.py              # Gradio app
└── render.yaml         # (old Render config, can ignore)
```