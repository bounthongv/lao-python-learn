FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway sets PORT environment variable
ENV PORT=7860

# Use Gradio's built-in production server flags
CMD ["sh", "-c", "python app.py --port $PORT --no-browser"]
