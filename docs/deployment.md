# Lao Python Learning Platform - Deployment Guide

## Quick Deploy to Hugging Face Spaces

### Option 1: Command Line (Recommended)

```bash
# Login to Hugging Face
huggingface-cli login

# Create new space
huggingface-cli repo create lao-python-learn --type space --space-sdk gradio

# Upload files
cd /home/bounthong/elearning-python/lao-python-learn
huggingface-cli upload bounthong/lao-python-learn . --repo-type space
```

### Option 2: Web Interface

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name: `lao-python-learn`
4. SDK: Gradio
5. Copy these files:
   - `app.py`
   - `requirements.txt`

---

## Files Needed

- `app.py` - Main application (already created)
- `requirements.txt` - Dependencies (already created)

## Access URL

After deployment, access at:
```
https://huggingface.co/spaces/[YOUR_USERNAME]/lao-python-learn
```
