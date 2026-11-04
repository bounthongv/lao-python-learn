# AGENTS.md — lao-python-learn

Quick-ramp file for this repo. Only high-signal facts.

## Python version
- Must use Python 3.12 (see `.python-version`, `runtime.txt`, `render.yaml`).
- The workspace `venv/` was originally a Linux venv (`bin/`, `lib/`); recreate on Windows:
  ```powershell
  py -3.12 -m venv venv
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

## Dependency trap (verified from clean install)
- Gradio 4.29.0 breaks with Starlette >= 1.0 (`TemplateResponse` signature removed), producing HTTP 500.
- `requirements.txt` pins: `fastapi==0.111.0`, `starlette==0.37.2`, `websockets==11.0.3`.
- Do NOT remove these pins.

## Database / Supabase
- Connection uses `DATABASE_URL` (Render convention) or individual `DB_*` env vars.
- `get_db_connection()` in `app.py` normalizes `postgres://` → `postgresql://` and adds `sslmode=require` when host is not localhost.
- Migration script: `migrate_to_supabase.py` (fixed to use `Path(__file__).parent` and `encoding="utf-8"` for Lao SQL). Run with `python migrate_to_supabase.py` inside the activated venv.
- Render `DATABASE_URL`: set in dashboard (transaction pooler, port 6543 is fine for app; direct/session preferred for migration), with `sync: false` in `render.yaml`.

## Render deploy
- `runtime: python` (not deprecated `env: python`).
- Build: `pip install --no-cache-dir -r requirements.txt` (no `--only-binary=:all:` needed with pins).
- Start: `python app.py --port $PORT` (no `--no-browser`; `Dockerfile` fixed).
- `PYTHON_VERSION=3.12.3` env var added.

## App startup behavior
- Loads all `ALL_LESSONS` from DB at import time. If DB unreachable, prints a warning and serves with empty lessons.
- `audioop` stub included for Python 3.14+ compatibility.

## Ignore / untracked
- `deploy_hf_new.py` has Linux-only paths (`/home/bounthong/...`, `/tmp/hf_token.txt`) — unrelated to Render work.
- `.dockerignore` excludes `venv/`, `docs/`, `.gradio/`.

## Verification sequence
```powershell
# 1. clean venv with 3.12
# 2. install
pip install -r requirements.txt
# 3. DB config
$env:SUPABASE_DB_URL='postgresql://...'
# 4. migrate
python migrate_to_supabase.py
# 5. start locally
python app.py --port 7860
```
