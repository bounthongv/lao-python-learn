# Deployment Guide — Lao Python Learning Platform

## Summary: Free Hosting Options

| Service | Free Tier | Difficulty | Your Choice |
|---------|-----------|------------|-------------|
| **Render** | 512MB RAM, 5GB bandwidth | Easy | ✅ RECOMMENDED |
| **Google Cloud Run** | 2M invocations/month | Medium | Alternative |
| **Hugging Face** | Static only (PRO needed for Gradio) | Hard | Already created |
| **PythonAnywhere** | Limited free | Easy | Not recommended |

---

## Firestore Clarification
Firestore = Database (stores data). NOT a hosting service.
- Cannot run Python/Gradio
- Can store quiz scores/results if needed later
- Would need Cloud Run or similar to host the app

---

## Option 1: Render (RECOMMENDED)

### Setup (5 minutes):
1. Create GitHub repo with this code
2. Sign up at https://render.com (use GitHub login)
3. Click "New" → "Web Service"
4. Connect your repository
5. Deploy!

### Manual Steps:
```bash
# On your local machine (Windows):
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/lao-python-learn.git
git push -u origin main
```

### Render Configuration:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gradio app.py --server.port $PORT --server.host 0.0.0.0`
- Env: PYTHON_VERSION=3.12

**Result:** https://lao-python-learn.onrender.com

---

## Option 2: Google Cloud Run

### Setup:
1. Create project at https://console.cloud.google.com
2. Enable Cloud Run API
3. Build Docker image:
```bash
docker build -t gcr.io/YOUR_PROJECT/lao-python-learn:latest .
docker push gcr.io/YOUR_PROJECT/lao-python-learn:latest
```
4. Deploy to Cloud Run

**Free Tier:** 2M invocations/month

---

## What I've Prepared

Files in `/home/bounthong/elearning-python/lao-python-learn/`:
- `render.yaml` - Render deployment config
- `deploy_render.py` - Python deploy script
- `deploy_render.sh` - Shell deploy script
- `DEPLOY.md` - This guide
- `requirements.txt` - Updated with python-dotenv

---

## Recommended Next Steps

1. Install git on your Windows machine
2. Push code to GitHub
3. Connect to Render
4. Deploy

Or I can guide you through any of these steps.
