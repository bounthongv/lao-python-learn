"""
Lao Python Learning Platform - Deployment Configuration
For Hugging Face Spaces
"""

# This file is used by Hugging Face Spaces
# The main app is in app.py

if __name__ == "__main__":
    import gradio as gr
    from app import app
    app.launch()
