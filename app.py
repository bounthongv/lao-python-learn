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

# Fix Jinja2 cache key error in Gradio 4.44.x / Python 3.14
# Gradio's internal templates pass a dict in the cache key tuple
# Patch Jinja2's LRUCache to handle unhashable dict keys
import jinja2.utils

# Helper to convert unhashable keys
def _make_hashable(key):
    if isinstance(key, tuple):
        return tuple(str(k) if isinstance(k, dict) else k for k in key)
    return key

# Patch __getitem__
_original_getitem = jinja2.utils.LRUCache.__getitem__
def _patched_getitem(self, key):
    try:
        return _original_getitem(self, key)
    except TypeError as e:
        if "unhashable type: 'dict'" in str(e):
            return _original_getitem(self, _make_hashable(key))
        raise
jinja2.utils.LRUCache.__getitem__ = _patched_getitem

# Patch __setitem__
_original_setitem = jinja2.utils.LRUCache.__setitem__
def _patched_setitem(self, key, value):
    try:
        return _original_setitem(self, key, value)
    except TypeError as e:
        if "unhashable type: 'dict'" in str(e):
            return _original_setitem(self, _make_hashable(key), value)
        raise
jinja2.utils.LRUCache.__setitem__ = _patched_setitem

# Patch __contains__
_original_contains = jinja2.utils.LRUCache.__contains__
def _patched_contains(self, key):
    try:
        return _original_contains(self, key)
    except TypeError as e:
        if "unhashable type: 'dict'" in str(e):
            return _original_contains(self, _make_hashable(key))
        raise
jinja2.utils.LRUCache.__contains__ = _patched_contains

# Fix Jinja2 split_template_path error: Gradio passes dict as template name
# Patch to handle dict input by converting to string
import jinja2.loaders
_original_split = jinja2.loaders.split_template_path
def _patched_split(template):
    if isinstance(template, dict):
        # Gradio bug: passes context dict as template name
        # Convert to string representation
        template = str(template)
    return _original_split(template)
jinja2.loaders.split_template_path = _patched_split

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
    "th": {"name": "Thai", "native": "ไทย", "flag": "🇹🇭"},
    "zh": {"name": "Chinese", "native": "中文", "flag": "🇨🇳"},
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
            "3. ລູກສອນ",
            "4. ລິສັດ",
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
    "th": {
        "title": "เรียน Python",
        "tab_lessons": "📚 บทเรียน",
        "tab_playground": "💻 เขียนโค้ด",
        "tab_about": "ℹ️ เกี่ยวกับ",
        "select_lesson": "เลือกบทเรียน",
        "playground_title": "เขียนโค้ด Python แล้วกด Run",
        "example_label": "ตัวอย่าง",
        "code_label": "โค้ด",
        "code_placeholder": "เขียนโค้ด Python ที่นี่...",
        "output_label": "ผลลัพธ์",
        "run_btn": "▶ Run",
        "success": "✅ สำเร็จ!",
        "success_no_output": "✅ สำเร็จ! (ไม่มีผลลัพธ์)",
        "error": "❌ ข้อผิดพลาด:",
        "about_title": "### เกี่ยวกับคอร์สนี้",
        "about_items": [
            "เรียน Python ด้วยภาษาของคุณ",
            "ออกแบบสำหรับนักเรียนมัธยม",
            "ไม่ต้องมีพื้นฐานการเขียนโปรแกรม",
            "รันโค้ดทันทีในเบราว์เซอร์",
        ],
        "lessons_list": [
            "1. พื้นฐาน Python",
            "2. เงื่อนไข",
            "3. วนลูป",
            "4. รายการ",
            "5. ฟังก์ชัน",
        ],
        "lang_label": "ภาษา",
    },
    "zh": {
        "title": "学习 Python",
        "tab_lessons": "📚 课程",
        "tab_playground": "💻 代码练习",
        "tab_about": "ℹ️ 关于",
        "select_lesson": "选择课程",
        "playground_title": "编写 Python 代码并点击运行",
        "example_label": "示例",
        "code_label": "代码",
        "code_placeholder": "在此编写 Python 代码...",
        "output_label": "输出",
        "run_btn": "▶ 运行",
        "success": "✅ 成功!",
        "success_no_output": "✅ 成功! (无输出)",
        "error": "❌ 错误:",
        "about_title": "### 关于本课程",
        "about_items": [
            "用您的语言学习 Python",
            "专为中学生设计",
            "无需编程基础",
            "浏览器中即时运行代码",
        ],
        "lessons_list": [
            "1. Python 基础",
            "2. 条件判断",
            "3. 循环",
            "4. 列表",
            "5. 函数",
        ],
        "lang_label": "语言",
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
    # Support both individual env vars and DATABASE_URL (Render convention)
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Parse DATABASE_URL: postgres://user:pass@host:port/db
        from urllib.parse import urlparse
        parsed = urlparse(db_url)
        return psycopg2.connect(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password,
            cursor_factory=RealDictCursor
        )
    
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "lao_python_learn"),
        user=os.environ.get("DB_USER", "lao_user"),
        password=os.environ.get("DB_PASSWORD", "lao_learn_2026"),
        cursor_factory=RealDictCursor
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
    "th": {
        "Hello World": 'print("สวัสดี! เรียน Python")',
        "Calculator": """# เครื่องคิดเลขง่ายๆ
a = 10
b = 3

print(a, "+", b, "=", a + b)
print(a, "-", b, "=", a - b)
print(a, "*", b, "=", a * b)
print(a, "/", b, "=", round(a / b, 4))
""",
        "Counting": """# นับตัวเลข
for i in range(1, 11):
    print(i, end=" ")
print()

# นับถอยหลัง
for i in range(10, 0, -1):
    print(i, end=" ")
print("Go!")
""",
        "Temperature Converter": """# แปลงอุณหภูมิ
celsius = 36.6
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")
""",
    },
    "zh": {
        "Hello World": 'print("你好! 学习 Python")',
        "Calculator": """# 简单计算器
a = 10
b = 3

print(a, "+", b, "=", a + b)
print(a, "-", b, "=", a - b)
print(a, "*", b, "=", a * b)
print(a, "/", b, "=", round(a / b, 4))
""",
        "Counting": """# 计数
for i in range(1, 11):
    print(i, end=" ")
print()

# 倒计数
for i in range(10, 0, -1):
    print(i, end=" ")
print("Go!")
""",
        "Temperature Converter": """# 温度转换
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
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Lao:wght@400;500;600;700&family=Noto+Sans+Thai:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

body, .gradio-container, textarea, input, button, select, .tab-item, .block {
    font-family: 'Noto Sans Lao', 'Noto Sans Thai', 'Noto Sans SC', sans-serif !important;
}

.lesson-html {
    font-family: 'Noto Sans Lao', 'Noto Sans Thai', 'Noto Sans SC', sans-serif !important;
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

/* Language selector styling */
.lang-selector { margin-bottom: 10px; }
"""

# Build the Gradio app with language support
def build_app():
    with gr.Blocks(title="Learn Python", css=custom_css) as app:
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
                show_label=False
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
                placeholder=UI_TEXT[DEFAULT_LANG]["code_placeholder"]
            )
            code_output = gr.Textbox(label=UI_TEXT[DEFAULT_LANG]["output_label"], lines=10, interactive=False)
            
            run_btn = gr.Button(UI_TEXT[DEFAULT_LANG]["run_btn"], variant="primary")
            
            def on_select_example(example, lang):
                return EXAMPLE_CODES.get(lang, EXAMPLE_CODES["lo"]).get(example, "")
            
            example_selector.change(on_select_example, inputs=[example_selector, lang_state], outputs=code_input)
            run_btn.click(run_code, inputs=[code_input, lang_state], outputs=code_output)
        
        with gr.Tab(UI_TEXT[DEFAULT_LANG]["tab_about"]) as tab_about:
            about_md = gr.Markdown(
                UI_TEXT[DEFAULT_LANG]["about_title"] + "\n" + 
                "\n".join([f"- {item}" for item in UI_TEXT[DEFAULT_LANG]["about_items"]]) + "\n\n" +
                "### Lessons\n" +
                "\n".join([f"{i+1}. {item}" for i, item in enumerate(UI_TEXT[DEFAULT_LANG]["lessons_list"])])
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
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=args.share,
        prevent_thread_lock=True,  # Required for Render's proxy
        show_error=True,
    )