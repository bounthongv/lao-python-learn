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
- Lesson `<pre>` blocks need `color: … !important` on `pre`, `pre code` **and** `pre code *`.
  Something inside the block sets its own dark token colour, which is invisible on the dark
  background; without `!important` the code samples render dark-on-dark.
- Exercise/solution markdown uses `elem_classes="exercise-md"`, deliberately NOT `lesson-html`:
  the light-on-dark rules above would make Gradio's own light code blocks unreadable.
- The lesson card is forced light (`background: #fafafa`), so it also needs `color: #1e293b
  !important`: `?__theme=dark` otherwise leaves `<li>`/`<td>` on the theme's light text colour,
  which is invisible on the card. Anything theme-coloured (the accordions, About) must NOT get a
  hard-coded colour — it breaks the other way.

## Lao terminology (use these, not literal dictionary words)
- List → ລິສ (not ລິສັດ = "company"), Loop → ລຸປ (not ລູກສອນ = "arrow"),
  variable → ຕົວແປ (not ຕົວແປງ), important → ສຳຄັນ (no ເ),
  string → ຄຳເວົ້າ (not ສາຍອັກສອນ, and not ຂໍ້ຄວາມ = "message/text").
- Write the ຳ vowel as U+0EB3 (ຄຳ, ຈຳນວນ), never ຄໍາ with U+0EC5 — that one means "neck".
- Much of the lesson prose is still machine-mangled Lao; fix it with byte-exact extracted
  strings, and never rewrite a whole lesson in one pass.

## Adding a lesson / language
- Lesson text lives in Postgres (`lessons`: `lang`, `title`, `slug`, `content_markdown`,
  `example_code`, `exercises_markdown`, `exercise_solutions`, `"order"`). Quote `"order"` in
  SQL — it needs escaping.
- `ALL_LESSONS` / `ALL_LESSON_HTML` are built at import time for every key in `LANGUAGES`;
  if the DB is unreachable or unmigrated the app still serves, with empty lessons.
- A new language needs parallel entries in `LANGUAGES`, `UI_TEXT`, and `EXAMPLE_CODES`, plus
  a SQL file of lessons with its own `lang` value and unique slugs (the `-en` suffix pattern).
- Only `lo` and `en` exist now. Thai and Chinese were removed at the owner's request; the
  English lessons in `init_db_en.sql` are the reference text the Lao is translated from — keep
  them section-by-section parallel when editing either side.
- `migrate_to_supabase.py` runs `init_db.sql` → `migrate_multilingual.sql` → `init_db_en.sql`.
  The last one needs the `lang` column, so it must stay after the multilingual migration.
  Lao rows in `init_db.sql` therefore must NOT mention the `lang` column.
- Lao and English both have lessons 1-8 now. Lessons 6-8 carry `exercises_markdown` +
  `exercise_solutions` inside their own INSERT instead of a later UPDATE, so prose and tasks
  stay together. `-- Lessons 6-8` marks that block in both SQL files.
- Lesson titles already include their number (`6. ວັດຈະນານຸກົມ (Dictionaries)`), and
  `ALL_LESSONS` is keyed by title. Anything that lists them must not renumber.
- The About tab lesson list comes from the DB through `about_markdown(lang)`, not from
  `UI_TEXT`; only the `### Lessons` heading text (`lessons_heading`) is hardcoded.
- README.md YAML front matter is the Hugging Face Spaces config; keep `sdk_version` in sync
  with `requirements.txt`.

## App startup behavior (app.py)
- Layout/`Button` components in an `outputs=[…]` list must be updated by returning a component
  object (`gr.Tab(label)`), never a bare string: Gradio raises
  `Tab Component not a valid output component` and the whole event fails with an "Error" toast.
  This silently broke the language switch until `show_error=True` was used to surface it.
- The `audioop`/`pyaudioop` stub must execute BEFORE `import gradio`; moving it breaks 3.14+.
- `RENDER=true` monkey-patches `gradio.networking.url_ok` to return True — Gradio 4.44 still
  fails its localhost check behind Render's reverse proxy. Do not remove.
- Port resolution: `--port` flag, else `$PORT`, else 7860. Start is `python app.py --port $PORT`.
- Playground runs user code with in-process `exec()` and redirected stdout. No sandbox and no
  subprocess; don't "harden" it by adding dependencies unless asked.
- `run_code()` also swaps `sys.stdin` for a `StringIO` of the Input textbox, which is how
  `input()` works. Blank input means `input()` raises `EOFError` — that is the intended message.
- `run_code()` runs `textwrap.dedent()` first: code pasted from a lesson keeps the block's
  indentation and Python rejects a first line that is indented. Only strips a *shared* prefix,
  so genuinely mis-indented snippets still get `unexpected indent`.
- `select_lesson()` returns 4 values (html, exercises, solutions, accordion update) and
  `on_lang_change()` returns 18; both must stay index-aligned with the `outputs=[…]` lists.
- Lessons with no `exercises_markdown` (Lao lessons 1-5 for now) hide the whole "Try it"
  accordion, so a half-translated lesson never shows an empty box.

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
