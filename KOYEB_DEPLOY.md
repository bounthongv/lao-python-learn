# Deploy Lao Python Learning Platform to Koyeb

## Why Koyeb?
- ✅ **Genuine free tier** (no credit card required for free tier)
- ✅ Works in Laos (global edge network)
- ✅ Native Docker support (uses your existing Dockerfile)
- ✅ **Free managed PostgreSQL** (1GB storage, shared CPU)
- ✅ Global edge deployment (low latency)
- ✅ Auto-deploy from GitHub

---

## Step 1: Prepare Your Code

Already ready:
- `Dockerfile` — Works with Koyeb (exposes PORT)
- `requirements.txt` — Python deps including psycopg2
- `app.py` — Loads lessons from PostgreSQL
- `init_db.sql` — Database initialization

---

## Step 2: Create Koyeb Account

1. Go to **https://koyeb.com**
2. Sign up with **GitHub** (recommended)
3. No credit card needed for free tier

---

## Step 3: Create PostgreSQL Database

1. In Koyeb dashboard → **Databases** → **Create Database**
2. Select **PostgreSQL**
3. **Plan**: Free (1GB storage, shared CPU)
4. **Region**: Choose closest (e.g., Singapore, Hong Kong)
5. **Name**: `lao-python-learn-db`
6. **Create**

Once created, note the **connection string** (format: `postgresql://user:pass@host:port/db`)

---

## Step 4: Deploy Web Service from GitHub

1. **Services** → **Create Service**
2. **GitHub** → Select `bounthongv/lao-python-learn`
3. **Builder**: Dockerfile (auto-detected)
4. **Instance**: Free (512MB RAM, shared CPU)
5. **Region**: Same as database (Singapore/Hong Kong)
6. **Port**: 7860 (Koyeb auto-detects from Dockerfile)
7. **Environment Variables** (add these):

| Key | Value |
|-----|-------|
| `DB_HOST` | `<from-db-connection-string>` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `<database-name>` |
| `DB_USER` | `<username>` |
| `DB_PASSWORD` | `<password>` |

> **Extract from connection string**: `postgresql://user:pass@host:5432/dbname`

8. **Deploy!**

---

## Step 5: Initialize Database

### Option A: Koyeb CLI (Recommended)
```bash
# Install Koyeb CLI
brew install koyeb/tap/koyeb  # macOS
# or: curl -fsSL https://cli.koyeb.com/install.sh | sh  # Linux

# Login
koyeb auth login

# Get database connection
koyeb databases get lao-python-learn-db --output json
```

### Option B: Web Console
1. Database → **Console** tab
2. Paste contents of `init_db.sql`
3. Run

### Option C: Local psql (if you have PostgreSQL client)
```bash
psql "postgresql://user:pass@host:5432/dbname" -f init_db.sql
```

---

## Step 6: Verify Deployment

1. Wait for build (2-3 minutes)
2. Click service URL: `https://<service-name>-<org>.koyeb.app`
3. Should see: **"ຮຽນ Python"** with 5 lessons

---

## Step 7: Custom Domain (Optional)

1. Service → **Settings** → **Domains**
2. Add your domain
3. Configure DNS CNAME to Koyeb's provided domain

---

## Koyeb Free Tier Limits

| Resource | Free Tier |
|----------|-----------|
| **Services** | 2 services |
| **RAM per service** | 512 MB |
| **CPU** | Shared |
| **Bandwidth** | 100 GB/month |
| **PostgreSQL** | 1 GB storage |
| **Build minutes** | 100/month |
| **Regions** | Global edge |

More than enough for a learning platform.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails | Check Dockerfile; ensure all deps in requirements.txt |
| App crashes | Check **Logs** tab; usually missing env vars |
| DB connection error | Verify env vars match database connection string |
| Lessons empty | Run `init_db.sql` on the database |
| Slow first load | Free tier spins down after inactivity (cold start ~10s) |

---

## Files for Koyeb

```
/home/bounthong/elearning-python/lao-python-learn/
├── Dockerfile          # ✅ Works with Koyeb
├── requirements.txt    # ✅ Python deps
├── app.py              # ✅ Gradio app
├── init_db.sql         # ✅ DB schema + 5 lessons
├── railway.json        # (for Railway, ignore)
├── render.yaml         # (for Render, ignore)
└── KOYEB_DEPLOY.md     # This guide
```

---

## Quick Deploy Checklist

- [ ] GitHub repo pushed (`git push origin main`)
- [ ] Koyeb account created
- [ ] PostgreSQL database created (free tier)
- [ ] Web service created from GitHub
- [ ] Environment variables set (DB_* from database connection)
- [ ] `init_db.sql` run on database
- [ ] Service URL accessible
- [ ] All 5 lessons displaying

---

## Cost: $0/month (Free Tier)

No credit card, no trial expiration — genuinely free for small apps.