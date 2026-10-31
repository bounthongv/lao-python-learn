"""
Lao Python Learning Platform
Web-based Python learning for Lao secondary students
Now with PostgreSQL database backend
"""

import os
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

# Database connection
def get_db_connection():
    """Get database connection from environment variables."""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "lao_python_learn"),
        user=os.environ.get("DB_USER", "lao_user"),
        password=os.environ.get("DB_PASSWORD", "lao_learn_2026"),
        cursor_factory=RealDictCursor
    )

def load_lessons_from_db():
    """Load lessons from PostgreSQL database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, slug, content_markdown, example_code, \"order\" FROM lessons ORDER BY \"order\"")
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
        # Fallback to empty dict - will use empty state
        return {}

# Load lessons from DB at startup
LESSONS = load_lessons_from_db()

# Pre-render all lessons to HTML at startup
LESSON_HTML = {name: render_md(data["content"]) for name, data in LESSONS.items()}

# Example codes for the code playground (static fallback)
EXAMPLE_CODES = {
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
"""
}

def run_code(code):
    """Run Python code and return output."""
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        exec(code)
        result = mystdout.getvalue()
        return f"✅ ສຳເລັດ!\n\n{result}" if result else "✅ ສຳເລັດ! (ບໍ່ມີຂອງອອກ)"
    except Exception as e:
        return f"❌ ຜິດພາດ:\n{str(e)}"
    finally:
        sys.stdout = old_stdout

def select_lesson(lesson_name):
    """Return pre-rendered HTML for the selected lesson."""
    if lesson_name and lesson_name in LESSON_HTML:
        return LESSON_HTML[lesson_name]
    return ""

first_lesson = list(LESSONS.keys())[0] if LESSONS else ""

# Custom CSS for Lao script + lesson styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Lao:wght@400;500;600;700&display=swap');

body, .gradio-container, textarea, input, button, select, .tab-item, .block {
    font-family: 'Noto Sans Lao', sans-serif !important;
}

.lesson-html {
    font-family: 'Noto Sans Lao', sans-serif !important;
    line-height: 1.8;
    padding: 10px;
}
.lesson-html h1 { font-size: 1.8em; font-weight: 700; margin-bottom: 0.5em; color: #1a1a2e; }
.lesson-html h2 { font-size: 1.4em; font-weight: 600; margin-top: 1.2em; margin-bottom: 0.4em; color: #16213e; }
.lesson-html p { margin-bottom: 0.8em; }
.lesson-html ul, .lesson-html ol { margin-left: 1.5em; margin-bottom: 0.8em; }
.lesson-html li { margin-bottom: 0.3em; }
.lesson-html code {
    font-family: 'Courier New', monospace !important;
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
}
.lesson-html pre {
    background: #1e1e2e;
    color: #cdd6f4;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin-bottom: 1em;
}
.lesson-html pre code {
    background: none;
    padding: 0;
    color: inherit;
}
"""

with gr.Blocks(title="ຮຽນ Python") as app:
    gr.Markdown("# 🐍 ຮຽນ Python")

    with gr.Tab("📚 ບົດຮຽນ"):
        lesson_selector = gr.Dropdown(
            choices=list(LESSONS.keys()),
            value=first_lesson,
            label="ເລືອກບົດຮຽນ"
        )
        # Use gr.HTML instead of gr.Markdown to bypass Gradio 6.x lazy hydration bug
        lesson_content = gr.HTML(
            value=LESSON_HTML.get(first_lesson, ""),
            show_label=False
        )

        lesson_selector.change(
            fn=select_lesson,
            inputs=lesson_selector,
            outputs=lesson_content
        )

    with gr.Tab("💻 ລອງຂຽນໂຄດ"):
        gr.Markdown("### ລອງຂຽນໂຄດ Python ແລ້ວກົດ Run")

        example_selector = gr.Dropdown(
            choices=list(EXAMPLE_CODES.keys()),
            value="Hello World",
            label="ຕົວຢ່າງ"
        )
        code_input = gr.Textbox(
            label="Code",
            lines=10,
            placeholder="ຂຽນໂຄດ Python ທີ່ນີ..."
        )
        code_output = gr.Textbox(label="ຜົນລັບ", lines=10, interactive=False)

        run_btn = gr.Button("▶ Run", variant="primary")

        def on_select_example(example):
            return EXAMPLE_CODES.get(example, "")

        example_selector.change(on_select_example, inputs=example_selector, outputs=code_input)
        run_btn.click(run_code, inputs=code_input, outputs=code_output)

    with gr.Tab("ℹ️ ກ່ຽວກັບ"):
        gr.Markdown("""
### ກ່ຽວກັບຄອສເລ
- ຮຽນ Python ພາສາລາວ
- ເໝາະສຳລັບນັກຮຽນມັດທະຍົມ
- ບໍ່ຕ້ອງການພື້ນຖານການຂຽນໂປຣແກຣມ
- ລອງຂຽນໂຄດໄດ້ທັນທີ

### ບົດຮຽນ
1. ພື້ນຖານ Python
2. ໃຊ້ງານເງື່ອນໄຂ
3. ລູກສອນ
4. ລິສັດ
5. ຟັງຊັນ
""")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="Create a temporary Gradio public link")
    parser.add_argument("--port", type=int, default=None, help="Port override")
    args = parser.parse_args()
    # Render sets PORT env var; fall back to --port flag or 7860
    port = args.port or int(os.environ.get("PORT", 7860))
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=args.share,
        css=custom_css,
    )