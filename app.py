"""
Lao Python Learning Platform
Web-based Python learning for Lao secondary students
Now with PostgreSQL database backend + Multilingual support
"""

import os
import sys

# Patch audioop for Python 3.14+ before importing gradio
try:
    import audioop
except ImportError:
    # audioop removed in Python 3.14, create stub AND register in sys.modules
    import types
    audioop = types.ModuleType('audioop')
    # Register the stub module so pydub can import it
    sys.modules['audioop'] = audioop
    sys.modules['pyaudioop'] = audioop  # pydub uses "import pyaudioop as audioop"
    # Add minimal stubs for pydub's requirements
    for name in ['getsample', 'max', 'maxpp', 'minmax', 'sum', 'sum2',
                 'avg', 'rms', 'rate', 'tiny', 'tiny32', 'tiny16', 'tiny8']:
        def stub_func(*args, **kwargs):
            return 0
        setattr(audioop, name, stub_func)

import gradio as gr
from markdown_it import MarkdownIt
import psycopg2
from psycopg2.extras import RealDictCursor

# Pre-render markdown to HTML using markdown-it
md = MarkdownIt("commonmark", {"html": True})

def render_md(text):
    """Convert markdown text to styled HTML."""
    html = md.render(text)
    return f'<div class="lesson-html">{html}</div>'

# ===================== MULTILINGUAL SUPPORT =====================

# Supported languages
LANGUAGES = {
    "lo": {"name": "ລາວ", "native": "ລາວ", "flag": "🇱🇦"},
    "en": {"name": "English", "native": "English", "flag": "🇺🇸"},
}

DEFAULT_LANG = os.environ.get("DEFAULT_LANG", "lo")

# UI Translations dictionary
UI_TEXT = {
    "lo": {
        "title": "ຮຽນ Python",
        "tab_lessons": "📚 ບົດຮຽນ",
        "tab_playground": "💻 ລອງຂຽນໂຄດ",
        "tab_about": "ℹ️ ກ່ຽວກັບ",
        "select_lesson": "ເລືອກບົດຮຽນ",
        "playground_title": "ລອງຂຽນໂຄດ Python ແລ້ວກົດ Run",
        "example_label": "ຕົວຢ່າງ",
        "code_label": "Code",
        "code_placeholder": "ຂຽນໂຄດ Python ທີ່ນີ...",
        "output_label": "ຜົນລັບ",
        "run_btn": "▶ Run",
        "success": "✅ ສຳເລັດ!",
        "success_no_output": "✅ ສຳເລັດ! (ບໍ່ມີຂອງອອກ)",
        "error": "❌ ຜິດພາດ:",
        "about_title": "### ກ່ຽວກັບຄອສເລ",
        "about_items": [
            "ຮຽນ Python ພາສາລາວ",
            "ເໝາະສຳລັບນັກຮຽນມັດທະຍົມ",
            "ບໍ່ຕ້ອງການພື້ນຖານການຂຽນໂປຣແກຣມ",
            "ລອງຂຽນໂຄດໄດ້ທັນທີ",
        ],
        "lessons_list": [
            "1. ພື້ນຖານ Python",
            "2. ໃຊ້ງານເງື່ອນໄຂ",
            "3. ລຸປ",
            "4. ລິສ",
            "5. ຟັງຊັນ",
        ],
        "lang_label": "ພາສາ / Language",
    },
    "en": {
        "title": "Learn Python",
        "tab_lessons": "📚 Lessons",
        "tab_playground": "💻 Playground",
        "tab_about": "ℹ️ About",
        "select_lesson": "Select Lesson",
        "playground_title": "Write Python Code & Click Run",
        "example_label": "Examples",
        "code_label": "Code",
        "code_placeholder": "Write your Python code here...",
        "output_label": "Output",
        "run_btn": "▶ Run",
        "success": "✅ Success!",
        "success_no_output": "✅ Success! (no output)",
        "error": "❌ Error:",
        "about_title": "### About This Course",
        "about_items": [
            "Learn Python in your language",
            "Designed for secondary students",
            "No programming experience needed",
            "Run code instantly in browser",
        ],
        "lessons_list": [
            "1. Python Basics",
            "2. Conditions",
            "3. Loops",
            "4. Lists",
            "5. Functions",
        ],
        "lang_label": "Language",
    },
}

def t(lang, key):
    """Get translated text for key in language."""
    return UI_TEXT.get(lang, UI_TEXT["lo"]).get(key, key)

def get_lang_choices():
    """Return language choices for dropdown."""
    return [(f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['native']}", code) for code in LANGUAGES]

# Database connection
def get_db_connection():
    """Get database connection from environment variables."""
    # Support both individual env vars and DATABASE_URL (Render/Supabase convention)
    db_url = os.environ.get("DATABASE_URL", "").strip()
    if db_url:
        # psycopg2 accepts a libpq URL directly. Only normalize the scheme
        # because Render sometimes hands out postgres:// URLs.
        if db_url.startswith("postgres://"):
            db_url = "postgresql://" + db_url[len("postgres://"):]

        # Managed Postgres (Supabase) requires TLS. Be explicit instead of
        # relying on libpq's sslmode=prefer.
        from urllib.parse import urlparse
        host = (urlparse(db_url).hostname or "").lower()
        if "sslmode=" not in db_url and host not in ("localhost", "127.0.0.1", "::1"):
            db_url += ("&" if "?" in db_url else "?") + "sslmode=require"

        return psycopg2.connect(
            db_url,
            cursor_factory=RealDictCursor,
            connect_timeout=10,
        )

    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "lao_python_learn"),
        user=os.environ.get("DB_USER", "lao_user"),
        password=os.environ.get("DB_PASSWORD", "lao_learn_2026"),
        cursor_factory=RealDictCursor,
        connect_timeout=10,
    )

def load_lessons_from_db(lang=DEFAULT_LANG):
    """Load lessons from PostgreSQL database for given language."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, slug, content_markdown, example_code, \"order\" FROM lessons WHERE lang = %s ORDER BY \"order\"",
            (lang,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        lessons = {}
        for row in rows:
            lessons[row["title"]] = {
                "content": row["content_markdown"],
                "example": row["example_code"] or ""
            }
        return lessons
    except Exception as e:
        print(f"Database error: {e}")
        return {}

def load_all_lessons():
    """Load lessons for all languages at startup."""
    all_lessons = {}
    for lang in LANGUAGES:
        all_lessons[lang] = load_lessons_from_db(lang)
    return all_lessons

# Load lessons for all languages at startup
ALL_LESSONS = load_all_lessons()
if not any(ALL_LESSONS.values()):
    print(
        "WARNING: No lessons were loaded from the database. "
        "Check that DATABASE_URL is set and that migrate_to_supabase.py has been run."
    )

# Pre-render all lessons to HTML for all languages
ALL_LESSON_HTML = {}
for lang, lessons in ALL_LESSONS.items():
    ALL_LESSON_HTML[lang] = {name: render_md(data["content"]) for name, data in lessons.items()}

# Example codes for the code playground (static fallback) - can be extended per language
EXAMPLE_CODES = {
    "lo": {
        "Hello World": 'print("ສະບາຍດີ! ລົດ Python")',
        "Calculator": """# ເຄື່ອງຄິດໄລ່ງ່າຍໆ (run once with fixed numbers)
a = 10
b = 3

print(a, "+", b, "=", a + b)
print(a, "-", b, "=", a - b)
print(a, "*", b, "=", a * b)
print(a, "/", b, "=", round(a / b, 4))
""",
        "Counting": """# ນັບຈຳນວນ
for i in range(1, 11):
    print(i, end=" ")
print()

# ນັບຍ້ອນຫຼັງ
for i in range(10, 0, -1):
    print(i, end=" ")
print("Go!")
""",
        "Temperature Converter": """# ປ່ຽນອຸນຫະພູມ (fixed input for playground)
celsius = 36.6
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")
""",
    },
    "en": {
        "Hello World": 'print("Hello! Learn Python")',
        "Calculator": """# Simple Calculator
a = 10
b = 3

print(a, "+", b, "=", a + b)
print(a, "-", b, "=", a - b)
print(a, "*", b, "=", a * b)
print(a, "/", b, "=", round(a / b, 4))
""",
        "Counting": """# Counting
for i in range(1, 11):
    print(i, end=" ")
print()

# Count down
for i in range(10, 0, -1):
    print(i, end=" ")
print("Go!")
""",
        "Temperature Converter": """# Temperature Converter
celsius = 36.6
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")
""",
    },
}

def run_code(code, lang):
    """Run Python code and return output with localized messages."""
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        exec(code)
        result = mystdout.getvalue()
        success_msg = t(lang, "success")
        no_output_msg = t(lang, "success_no_output")
        return f"{success_msg}\n\n{result}" if result else no_output_msg
    except Exception as e:
        error_msg = t(lang, "error")
        return f"{error_msg}\n{str(e)}"
    finally:
        sys.stdout = old_stdout

def select_lesson(lesson_name, lang):
    """Return pre-rendered HTML for the selected lesson in given language."""
    if lesson_name and lang in ALL_LESSON_HTML and lesson_name in ALL_LESSON_HTML[lang]:
        return ALL_LESSON_HTML[lang][lesson_name]
    return ""

def get_first_lesson(lang):
    """Get first lesson title for given language."""
    lessons = ALL_LESSONS.get(lang, {})
    return list(lessons.keys())[0] if lessons else ""

# Custom CSS for multilingual support
# No @import (blocked on Render); use system font stack with Lao/Thai/Chinese coverage
custom_css = """
/* === Base font stack === */
body, .gradio-container, textarea, input, button, select, .tab-item, .block {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Lao', 'Noto Sans Thai', 'Noto Sans SC', 'Helvetica Neue', Arial, sans-serif !important;
}

/* === Layout containers === */
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 24px 16px !important;
}
#main { padding: 0 !important; }

/* === Tabs === */
.tab-nav { 
    border-bottom: 2px solid #e2e8f0; 
    margin-bottom: 24px; 
}
.tab-item {
    font-weight: 500 !important;
    padding: 12px 20px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s ease;
}
.tab-item.selected {
    background: #e0e7ff !important;
    color: #3730a3 !important;
    border-bottom-color: #6366f1 !important;
}

/* === Language selector === */
.lang-selector { 
    margin-bottom: 16px !important; 
}
.lang-selector select { 
    min-width: 200px; 
}

/* === Lesson content === */
.lesson-html,
.lesson-html > .lesson-html {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Lao', 'Noto Sans Thai', 'Noto Sans SC', 'Helvetica Neue', Arial, sans-serif !important;
    line-height: 1.8;
    padding: 16px;
    background: #fafafa;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    overflow-wrap: break-word;
    word-break: keep-all;
    max-width: 100%;
}
.lesson-html h1, .lesson-html > .lesson-html h1 { font-size: 1.8em; font-weight: 700; margin-bottom: 0.5em; color: #1a1a2e; }
.lesson-html h2, .lesson-html > .lesson-html h2 { font-size: 1.4em; font-weight: 600; margin-top: 1.2em; margin-bottom: 0.4em; color: #16213e; }
.lesson-html h3, .lesson-html > .lesson-html h3 { font-size: 1.2em; font-weight: 600; margin-top: 1em; margin-bottom: 0.3em; color: #1e293b; }
.lesson-html h4, .lesson-html > .lesson-html h4 { font-size: 1.1em; font-weight: 600; margin-top: 1em; margin-bottom: 0.3em; color: #334155; }
.lesson-html h5, .lesson-html > .lesson-html h5,
.lesson-html h6, .lesson-html > .lesson-html h6 { font-size: 1em; font-weight: 600; margin-top: 1em; margin-bottom: 0.3em; color: #475569; }
.lesson-html p, .lesson-html > .lesson-html p { margin-bottom: 0.8em; color: #1e293b; }
.lesson-html ul, .lesson-html ol, .lesson-html > .lesson-html ul, .lesson-html > .lesson-html ol { margin-left: 1.5em; margin-bottom: 0.8em; }
.lesson-html li, .lesson-html > .lesson-html li { margin-bottom: 0.3em; }
.lesson-html li::marker { color: #6366f1; font-weight: 600; }

/* Inline code */
.lesson-html code, .lesson-html > .lesson-html code {
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
    color: #e11d48;
}

/* Code blocks. The dark background needs !important on the text colour too:
   something inside <pre> sets its own dark token colour, which renders
   invisible against #0f172a. */
.lesson-html pre, .lesson-html > .lesson-html pre {
    background: #0f172a !important;
    color: #e2e8f0 !important;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1em;
    border: 1px solid #1e293b;
}
.lesson-html pre code, .lesson-html > .lesson-html pre code,
.lesson-html pre code *, .lesson-html > .lesson-html pre code * {
    background: none !important;
    padding: 0;
    color: #e2e8f0 !important;
    font-size: 0.9em;
    line-height: 1.6;
}

/* Blockquotes */
.lesson-html blockquote, .lesson-html > .lesson-html blockquote {
    border-left: 4px solid #6366f1;
    padding-left: 16px;
    margin: 1em 0;
    color: #475569;
    font-style: italic;
    background: #f8fafc;
    border-radius: 0 8px 8px 0;
    padding: 8px 16px;
}

/* Tables */
.lesson-html table, .lesson-html > .lesson-html table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.95em;
}
.lesson-html th, .lesson-html td, .lesson-html > .lesson-html th, .lesson-html > .lesson-html td {
    border: 1px solid #e2e8f0;
    padding: 8px 12px;
    text-align: left;
}
.lesson-html th, .lesson-html > .lesson-html th {
    background: #f1f5f9;
    font-weight: 600;
    color: #1e293b;
}
.lesson-html tr:nth-child(even), .lesson-html > .lesson-html tr:nth-child(even) {
    background: #fafafa;
}

/* Horizontal rule */
.lesson-html hr, .lesson-html > .lesson-html hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 2em 0;
}

/* Strong/Emphasis */
.lesson-html strong, .lesson-html > .lesson-html strong { font-weight: 700; color: #1a1a2e; }
.lesson-html em, .lesson-html > .lesson-html em { font-style: italic; color: #334155; }

/* Links */
.lesson-html a, .lesson-html > .lesson-html a {
    color: #6366f1;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}
.lesson-html a:hover, .lesson-html > .lesson-html a:hover {
    border-bottom-color: #6366f1;
}

/* === Playground === */
.code-editor textarea {
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    tab-size: 4 !important;
}
.run-btn { 
    min-width: 100px; 
}

/* === Dropdowns & Inputs === */
.gr-dropdown, .gr-textbox { 
    width: 100% !important; 
}

/* === About tab === */
.about-content {
    padding: 16px;
    line-height: 1.7;
}
"""

# Build the Gradio app with language support
def build_app():
    theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="slate",
    )
    with gr.Blocks(title="Learn Python", css=custom_css, theme=theme) as app:
        # Language selector at top
        lang_selector = gr.Dropdown(
            choices=get_lang_choices(),
            value=DEFAULT_LANG,
            label=UI_TEXT[DEFAULT_LANG]["lang_label"],
            elem_classes="lang-selector"
        )
        
        # Title
        title_md = gr.Markdown(f"# 🐍 {UI_TEXT[DEFAULT_LANG]['title']}")
        
        # State to hold current language
        lang_state = gr.State(DEFAULT_LANG)
        
        with gr.Tab(UI_TEXT[DEFAULT_LANG]["tab_lessons"]) as tab_lessons:
            first_lesson = get_first_lesson(DEFAULT_LANG)
            lesson_selector = gr.Dropdown(
                choices=list(ALL_LESSONS[DEFAULT_LANG].keys()),
                value=first_lesson,
                label=UI_TEXT[DEFAULT_LANG]["select_lesson"]
            )
            lesson_content = gr.HTML(
                value=ALL_LESSON_HTML[DEFAULT_LANG].get(first_lesson, ""),
                show_label=False,
                elem_classes="lesson-html"
            )
            
            lesson_selector.change(
                fn=select_lesson,
                inputs=[lesson_selector, lang_state],
                outputs=lesson_content
            )
        
        with gr.Tab(UI_TEXT[DEFAULT_LANG]["tab_playground"]) as tab_playground:
            playground_title_md = gr.Markdown(f"### {UI_TEXT[DEFAULT_LANG]['playground_title']}")
            
            example_selector = gr.Dropdown(
                choices=list(EXAMPLE_CODES[DEFAULT_LANG].keys()),
                value="Hello World",
                label=UI_TEXT[DEFAULT_LANG]["example_label"]
            )
            code_input = gr.Textbox(
                label=UI_TEXT[DEFAULT_LANG]["code_label"],
                lines=10,
                placeholder=UI_TEXT[DEFAULT_LANG]["code_placeholder"],
                elem_classes="code-editor"
            )
            code_output = gr.Textbox(label=UI_TEXT[DEFAULT_LANG]["output_label"], lines=10, interactive=False)
            
            run_btn = gr.Button(UI_TEXT[DEFAULT_LANG]["run_btn"], variant="primary", elem_classes="run-btn")
            
            def on_select_example(example, lang):
                return EXAMPLE_CODES.get(lang, EXAMPLE_CODES["lo"]).get(example, "")
            
            example_selector.change(on_select_example, inputs=[example_selector, lang_state], outputs=code_input)
            run_btn.click(run_code, inputs=[code_input, lang_state], outputs=code_output)
        
        with gr.Tab(UI_TEXT[DEFAULT_LANG]["tab_about"]) as tab_about:
            about_md = gr.Markdown(
                UI_TEXT[DEFAULT_LANG]["about_title"] + "\n" + 
                "\n".join([f"- {item}" for item in UI_TEXT[DEFAULT_LANG]["about_items"]]) + "\n\n" +
                "### Lessons\n" +
                "\n".join([f"{i+1}. {item}" for i, item in enumerate(UI_TEXT[DEFAULT_LANG]["lessons_list"])]),
                elem_classes="about-content"
            )
        
        # Language change handler - returns values for each output component
        def on_lang_change(lang):
            first = get_first_lesson(lang)
            lessons = list(ALL_LESSONS.get(lang, {}).keys())
            examples = list(EXAMPLE_CODES.get(lang, EXAMPLE_CODES["lo"]).keys())
            ui = UI_TEXT.get(lang, UI_TEXT["lo"])
            
            # Return values in order matching outputs list below
            return [
                # title_md
                f"# 🐍 {ui['title']}",
                # tab_lessons label
                ui['tab_lessons'],
                # lesson_selector (choices, value, label)
                gr.Dropdown(choices=lessons, value=first, label=ui['select_lesson']),
                # lesson_content
                ALL_LESSON_HTML[lang].get(first, ""),
                # tab_playground label
                ui['tab_playground'],
                # playground_title_md
                f"### {ui['playground_title']}",
                # example_selector
                gr.Dropdown(choices=examples, value="Hello World", label=ui['example_label']),
                # code_input (label, placeholder)
                gr.Textbox(label=ui['code_label'], placeholder=ui['code_placeholder']),
                # code_output (label)
                gr.Textbox(label=ui['output_label']),
                # run_btn
                gr.Button(ui['run_btn'], variant="primary"),
                # tab_about label
                ui['tab_about'],
                # about_md
                ui['about_title'] + "\n" + "\n".join([f"- {item}" for item in ui['about_items']]) + "\n\n### Lessons\n" + "\n".join([f"{i+1}. {item}" for i, item in enumerate(ui['lessons_list'])]),
                # lang_state
                lang,
                # lang_selector (label)
                gr.Dropdown(label=ui['lang_label']),
            ]
        
        lang_selector.change(
            fn=on_lang_change,
            inputs=lang_selector,
            outputs=[
                title_md,           # 0
                tab_lessons,        # 1
                lesson_selector,    # 2
                lesson_content,     # 3
                tab_playground,     # 4
                playground_title_md,# 5
                example_selector,   # 6
                code_input,         # 7
                code_output,        # 8
                run_btn,            # 9
                tab_about,          # 10
                about_md,           # 11
                lang_state,         # 12
                lang_selector,      # 13
            ]
        )
    
    return app

# Build app
app = build_app()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="Create a temporary Gradio public link")
    parser.add_argument("--port", type=int, default=None, help="Port override")
    args = parser.parse_args()
    # Render sets PORT env var; fall back to --port flag or 7860
    port = args.port or int(os.environ.get("PORT", 7860))

    # Gradio 4.44+ still fails localhost check on Render in some configs.
    # Monkey-patch url_ok() to always succeed when behind Render's reverse proxy.
    if os.environ.get("RENDER") == "true":
        import gradio.networking as _gn
        _gn.url_ok = lambda url: True

    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=args.share,
        inbrowser=False,
        quiet=True,
        root_path="/",
    )