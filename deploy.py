#!/usr/bin/env python3
"""
Hugging Face Space deployment script for Lao Python Learning Platform
"""

import subprocess
import sys
import os

SPACE_NAME = "bounthong/lao-python-learn"

def check_hf_login():
    """Check if user is logged into Hugging Face"""
    try:
        result = subprocess.run(
            ["huggingface-cli", "whoami"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ Logged in as: {result.stdout.strip()}")
            return True
        else:
            print("✗ Not logged into Hugging Face")
            return False
    except FileNotFoundError:
        print("✗ huggingface-cli not installed")
        return False

def create_readme():
    """Create README.md for Hugging Face Space"""
    readme_content = """---
tags:
- python
- education
- lao-language
- gradio
- machine-learning
datasets: []
metrics: []
license: mit
---

# 🐍 ຮຽນ Python ພາສາລາວ

Learn Python programming in Lao language. Designed for Lao secondary school students.

## Features
- 5 structured lessons in Lao language
- Interactive code execution
- Pre-loaded examples
- No login required

## Lessons
1. **Python Basics** - print(), variables, data types, arithmetic
2. **Conditional Logic** - if/elif/else
3. **Loops** - for and while loops
4. **Lists** - creating and using lists
5. **Functions** - defining and calling functions

## How to Use
1. Select a lesson from the dropdown
2. Read the explanation
3. Go to "Code" tab to try examples
4. Run code and see results

## Built With
- Python 3.12
- Gradio
- No external dependencies required

## Author
Created for Lao education

## License
MIT
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✓ Created README.md")

def run_app():
    """Run the Gradio app locally"""
    print("\n" + "="*50)
    print("Running Lao Python Learning Platform")
    print("="*50 + "\n")
    
    import gradio as gr
    
    # Import the app
    sys.path.insert(0, os.path.dirname(__file__))
    from app import app
    
    app.launch(share=True)

if __name__ == "__main__":
    if "--deploy" in sys.argv:
        if check_hf_login():
            create_readme()
            print("\n" + "="*50)
            print("To deploy, run:")
            print(f"  cd {os.getcwd()}")
            print("  huggingface-cli upload bounthong/lao-python-learn . --repo-type space")
            print("="*50)
    else:
        run_app()
