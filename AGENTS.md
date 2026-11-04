# AGENTS.md

This file provides guidance to the AI agent when working with code in this repository.

Quick-ramp file for this repo. Only high-signal facts.

## Python / venv
- Python 3.12 (see `.python-version`, `runtime.txt`, `render.yaml`).
- `venv/` here is a working Windows venv — use `venv/Scripts/python.exe` after
  `.\venv\Scripts\Activate.ps1`. Only recreate if it contains `bin/` + `lib/` (a leftover
  Linux venv): `py -3.12 -m venv venv && pip install -r requirements.txt`.

## Dependency pins (verified from clean install)
- Gradio 4.44.1 with `fastapi==0.115.0`, `starlette==0.38.6`, `websockets==12.0`.
- Starlette >= 1.0 removed the `TemplateResponse` signature Gradio calls → HTTP 500.
- `websockets` must be exactly `12.0`; `12.0.3` was never published (commit f4ee1ab).
- Do NOT remove or bump these pins.

## CSS gotchas (cost 4 fix commits)
- Gradio ignores plain selectors; styling requires `elem_classes="…"` on the component.
- `render_md()` wraps output in `<div class="lesson-html">` and `gr.HTML` adds its own wrapper,
  so content is double-wrapped: style both (`.lesson-html, .lesson-html > .lesson-html { … }`).
- Never `@import` webfonts — blocked on Render. Use the system font stack with `Noto Sans Lao`,
  `Noto Sans Thai`, `Noto Sans SC` fallbacks and `!important`.

## Adding a lesson / language
- Lesson text lives in Postgres (`lessons`: `lang`, `title`, `slug`, `content_markdown`,
  `example_code`, `"order"`). Quote `"order"` in SQL — it needs escaping.
- `ALL_LESSONS` / `ALL_LESSON_HTML` are built at import time for every key in `LANGUAGES`;
  if the DB is unreachable or unmigrated the app still serves, with empty lessons.
- A new language needs parallel entries in `LANGUAGES`, `UI_TEXT`, and `EXAMPLE_CODES`.
- README.md YAML front matter is the Hugging Face Spaces config; keep `sdk_version` in sync
  with `requirements.txt`.

## App startup behavior (app.py)
- The `audioop`/`pyaudioop` stub must execute BEFORE `import gradio`; moving it breaks 3.14+.
- `RENDER=true` monkey-patches `gradio.networking.url_ok` to return True — Gradio 4.44 still
  fails its localhost check behind Render's reverse proxy. Do not remove.
- Port resolution: `--port` flag, else `$PORT`, else 7860. Start is `python app.py --port $PORT`.
- Playground runs user code with in-process `exec()` and redirected stdout. No sandbox and no
  subprocess; don't "harden" it by adding dependencies unless asked.

## Database / Supabase
- The app reads `DATABASE_URL` (or individual `DB_*` vars); `migrate_to_supabase.py` reads
  `SUPABASE_DB_URL`. Two different variables — set both.
- `get_db_connection()` normalizes `postgres://` → `postgresql://` and appends
  `sslmode=require` when the host is not localhost.
- Migration SQL is Lao UTF-8; the script already uses `Path(__file__).parent` + `encoding="utf-8"`.
- Render `DATABASE_URL` is set in the dashboard (transaction pooler, port 6543, is fine for the
  app; direct/session connection preferred for migration) with `sync: false` in `render.yaml`.

## Render deploy
- `runtime: python` (not the deprecated `env: python`).
- Build: `pip install --no-cache-dir -r requirements.txt` (no `--only-binary=:all:` needed).
- `PYTHON_VERSION=3.12.3` env var.

## Repo etiquette
- Commits: `Fix: <what>` / `Upgrade: <what>`, imperative, no ticket prefixes. Work on `main`.
- Remotes: `origin` (GitHub → Render deploy target) and `hf` (Hugging Face Spaces). Never push
  to `hf` unless explicitly asked.
- `.gitignore` excludes `*.png` repo-wide; use `git add -f` for PNGs that are real assets.
- `deploy_*.py` / `deploy_*.sh` for Railway, Koyeb and HF are legacy (several contain Linux-only
  paths like `/home/bounthong/...`, `/tmp/hf_token.txt`). Render via `render.yaml` is live.

## Verification sequence
```powershell
# 1. activate venv (3.12)
.\venv\Scripts\Activate.ps1
# 2. install
pip install -r requirements.txt
# 3. DB config
$env:SUPABASE_DB_URL='postgresql://...'
# 4. migrate
python migrate_to_supabase.py
# 5. start locally
python app.py --port 7860
```
