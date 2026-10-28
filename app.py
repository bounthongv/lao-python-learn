"""
Lao Python Learning Platform
Web-based Python learning for Lao secondary students
"""

import gradio as gr
from markdown_it import MarkdownIt

# Pre-render markdown to HTML using markdown-it (bundled with Gradio)
md = MarkdownIt("commonmark", {"html": True})

def render_md(text):
    """Convert markdown text to styled HTML."""
    html = md.render(text)
    return f'<div class="lesson-html">{html}</div>'

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

# Lesson content in Lao
LESSONS = {
    "1. ພື້ນຖານ Python": {
        "content": """# ບົດທີ 1: ພື້ນຖານ Python

## 1.1 ການພິມຂໍ້ຄວາມ (Print)
ໃນ Python, ເຮົາໃຊ້ `print()` ເພື່ອສະແດງຜົນ:

```python
print("ສະບາຍດີ!")
print(10 + 5)
```

## 1.2 ຕົວປ່ຽນ (Variables)
ຕົວປ່ຽນແມ່ນສະຖານທີ່ເກັບຂໍ້ມູນ:

```python
name = "ສົມພູ"
age = 15
height = 170.5

print(name)
print(age)
```

## 1.3 ປະເພດຂໍ້ມູນ (Data Types)
- `str` - ຂໍ້ຄວາມ
- `int` - ຈຳນວນເຕັມ
- `float` - ຈຳນວນທົດສະນິຍົມ
- `bool` - ຄ່າຈິງ/ເທືອ

## 1.4 ການຄິດໄລ່ (Arithmetic)
```python
a = 10
b = 3
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3 (ຫານລວງ)
print(a % b)   # 1 (ເສດ)
print(a ** b)  # 1000 (ລົງກຳລັງ)
```
""",
        "example": """# ລອງຂຽນໂຄງການທຳອິດ
# (input() requires stdin — in the Gradio playground it's bypassed; use the
# calculator example for an interactive demo)
name = "ໂລກ Python"  # ໃຊ້ຕົວຢ່າງ
print("ສະບາຍດີ", name)
print("ຍິນດີຕ້ອນຮັບສູ່ໂລກ Python!")
"""
    },

    "2. ໃຊ້ງານເງື່ອນໄຂ": {
        "content": """# ບົດທີ 2: ໃຊ້ງານເງື່ອນໄຂ

## 2.1 If / Elif / Else
```python
age = 18

if age >= 18:
    print("ເຈົ້າເປັນຄົນຜູ້ໃຫຍ່")
elif age >= 15:
    print("ເຈົ້າເປັນໜຸ່ມ")
else:
    print("ເຈົ້າເປັນເດັກນ້ອຍ")
```

## 2.2 ເງື່ອນໄຂຄອມປາເລີ
- `==` (ເທົ່າກັບ)
- `!=` (ບໍ່ເທົ່າກັບ)
- `>` (ຫຼາຍກວ່າ)
- `<` (ໜ້ອຍກວ່າ)
- `>=` (ຫຼາຍກວ່າ ຫຼື ເທົ່າກັບ)
- `<=` (ໜ້ອຍກວ່າ ຫຼື ເທົ່າກັບ)
- `and`, `or`, `not`

## 2.3 ຕົວຢ່າງ
```python
score = 85

if score >= 80:
    print("A")
elif score >= 70:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```
""",
        "example": """# ກວດສອບອາຍຸ (fixed for playground; remove the input() call)
age = 20  # ໃສ່ຕົວເລກທີ່ຕ້ອງການ

if age < 0:
    print("ອາຍຸບໍ່ຖືກຕ້ອງ")
elif age < 13:
    print("ເດັກນ້ອຍ")
elif age < 18:
    print("ໜຸ່ມ")
else:
    print("ຜູ້ໃຫຍ່")
"""
    },

    "3. ລູກສອນ (Loops)": {
        "content": """# ບົດທີ 3: ລູກສອນ

## 3.1 For Loop
```python
# ປຸ່ມ 5 ຄັ້ງ
for i in range(5):
    print("ຄັ້ງທີ", i)

# ນັບຈາກ 1 ຫາ 10
for num in range(1, 11):
    print(num)
```

## 3.2 While Loop
```python
count = 0
while count < 5:
    print("count =", count)
    count += 1
```

## 3.3 Break ແລະ Continue
```python
for i in range(10):
    if i == 3:
        continue  # ຫຼີກລ່ຽງ 3
    if i == 7:
        break  # ຢຸດທີ່ 7
    print(i)
```
""",
        "example": """# ນັບຈົນກວ່າຈະພົບ 100 (no input needed)
total = 0
i = 1
while total < 100:
    total += i
    i += 1
print("ຜົນບວກ:", total)
"""
    },

    "4. ລິສັດ (Lists)": {
        "content": """# ບົດທີ 4: ລິສັດ

## 4.1 ສ້າງລິສັດ
```python
fruits = ["ແຟັສ", "ຕະຫຼອດ", "ມັນ"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "ສີ", 3.14, True]
```

## 4.2 ເຂົ້າເຖິງອົງປະກອບ
```python
fruits = ["ແຟັສ", "ຕະຫຼອດ", "ມັນ"]
print(fruits[0])  # ແຟັສ
print(fruits[-1])  # ມັນ
```

## 4.3 ລຽງລິສັດ
```python
nums = [3, 1, 4, 1, 5, 9]
nums.sort()
print(nums)  # [1, 1, 3, 4, 5, 9]

nums.reverse()
print(nums)  # [9, 5, 4, 3, 1, 1]
```

## 4.4 ເພີ່ມ/ຕັດ
```python
fruits = ["ແຟັສ", "ຕະຫຼອດ"]
fruits.append("ມັນ")  # ເພີ່ມຢູ່ທ້າຍ
fruits.insert(0, "ເລືອກ")  # ເພີ່ມຢູ່ຕຳແໜ່ງ
fruits.remove("ແຟັສ")  # ຕັດອອກ
popped = fruits.pop()  # ຕັດ ແລະ ກັບຄືນ
```
""",
        "example": """# ຈັດການລາຍການ (no input — demo loop)
shopping = ["ເປັດ", "ໄກ່"]
print("ເລີ່ມຕົ້ນ:", shopping)
shopping.append("ໄຂ່")
shopping.pop()
print("ຈົບ:", shopping)
"""
    },

    "5. ຟັງຊັນ (Functions)": {
        "content": """# ບົດທີ 5: ຟັງຊັນ

## 5.1 ສ້າງຟັງຊັນ
```python
def say_hello():
    print("ສະບາຍດີ!")

say_hello()
```

## 5.2 ຟັງຊັນທີ່ມີພາaráມິເຕີ
```python
def greet(name):
    print("ສະບາຍດີ", name)

greet("ສົມພູ")
```

## 5.3 ກັບຄືນຄ່າ
```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

## 5.4 Default Parameters
```python
def power(base, exp=2):
    return base ** exp

print(power(3))     # 9
print(power(2, 10)) # 1024
```
""",
        "example": """# ຄຳນວນພື້ນທີ່ວົງມົນ (no input — fixed radius)
def calculate_circle_area(radius):
    pi = 3.14159
    area = pi * radius ** 2
    return area

r = 5.0  # ລັດສະໝີ
print("ພື້ນທີ່:", calculate_circle_area(r))
"""
    }
}

# Pre-render all lessons to HTML at startup
LESSON_HTML = {name: render_md(data["content"]) for name, data in LESSONS.items()}

# Example codes for the code playground
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

first_lesson = list(LESSONS.keys())[0]

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
            value=LESSON_HTML[first_lesson],
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
    import os
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
