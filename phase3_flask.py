# Phase 3: Web Application with Flask

"""
Phase 3: Simple Web Application with Flask
Learning Objectives:
- HTTP requests and responses
- Routing
- Templates
- Building a complete web app
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for

app = Flask(__name__)

# ============================================================
# LESSON 1: Basic Routes and Responses
# ============================================================

@app.route('/')
def home():
    """Home page"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lao Python Web App - Lesson 1</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .lesson { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🐍 Lao Python Web Application</h1>
        <div class="lesson">
            <h2>Lesson 1: Basic Routes</h2>
            <p>Routes map URLs to Python functions:</p>
            <pre><code>@app.route('/')
def home():
    return "Hello World!"</code></pre>
        </div>
        
        <h3>Navigation:</h3>
        <a href="/about">About</a> | 
        <a href="/contact">Contact</a> |
        <a href="/api/data">API Data</a>
    </body>
    </html>
    '''
    return html


@app.route('/about')
def about():
    """About page"""
    return '<h1>About</h1><p>This is a Flask web application for learning Python.</p>'


@app.route('/contact')
def contact():
    """Contact page"""
    return '''
    <h1>Contact</h1>
    <form method="POST" action="/submit">
        <input type="text" name="name" placeholder="Your Name"><br>
        <input type="email" name="email" placeholder="Your Email"><br>
        <textarea name="message" placeholder="Your Message"></textarea><br>
        <button type="submit">Send</button>
    </form>
    '''


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    name = request.form.get('name', 'Anonymous')
    return f'<h1>Thanks {name}!</h1><p>Your message has been received.</p><a href="/">Back</a>'


# ============================================================
# LESSON 2: Templates
# ============================================================

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    
    <div class="card">
        <h2>{{ heading }}</h2>
        <p>{{ content }}</p>
    </div>
    
    {% if items %}
    <div class="card">
        <h2>Items</h2>
        <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <a href="/" class="btn">Home</a>
</body>
</html>
'''

@app.route('/template-demo')
def template_demo():
    """Demonstrate template rendering"""
    items = ["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template_string(TEMPLATE, 
                                  title="Template Demo",
                                  heading="Passing Variables to Templates",
                                  content="Flask templates make it easy to separate logic from presentation.",
                                  items=items)


# ============================================================
# LESSON 3: API Endpoints
# ============================================================

# In-memory "database"
tasks = []

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    for task in tasks:
        if task["id"] == task_id:
            data = request.get_json()
            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"})


@app.route('/api/data')
def api_data():
    """Simple API endpoint"""
    return jsonify({
        "message": "Hello from Flask API!",
        "timestamp": "2026-10-25",
        "version": "1.0"
    })


# ============================================================
# LESSON 4: Full Web App - Task Manager
# ============================================================

TASK_MANAGER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager - Lesson 4</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .task { display: flex; justify-content: space-between; align-items: center; 
                padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 5px; }
        .task.completed { text-decoration: line-through; opacity: 0.6; }
        .btn { padding: 8px 15px; margin: 0 5px; border: none; border-radius: 3px; cursor: pointer; }
        .btn-primary { background: #3498db; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-success { background: #2ecc71; color: white; }
        input[type="text"] { padding: 10px; width: 70%; border: 1px solid #ddd; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>📋 Task Manager</h1>
    
    <div class="add-task">
        <form method="POST" action="/tasks">
            <input type="text" name="title" placeholder="Add new task..." required>
            <button type="submit" class="btn btn-primary">Add</button>
        </form>
    </div>
    
    <div class="tasks">
    {% for task in tasks %}
        <div class="task {% if task.completed %}completed{% endif %}">
            <span>{{ task.title }}</span>
            <div>
                <a href="/tasks/{{ task.id }}/toggle" class="btn btn-success">✓</a>
                <a href="/tasks/{{ task.id }}/delete" class="btn btn-danger">✗</a>
            </div>
        </div>
    {% endfor %}
    </div>
    
    <p>Total: {{ tasks|length }} tasks | Completed: {{ tasks|selectattr("completed")|list|length }} tasks</p>
</body>
</html>
'''

@app.route('/tasks', methods=['GET'])
def list_tasks():
    """List all tasks"""
    return render_template_string(TASK_MANAGER_TEMPLATE, tasks=tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    title = request.form.get('title', '').strip()
    if title:
        tasks.append({
            "id": len(tasks) + 1,
            "title": title,
            "completed": False
        })
    return redirect(url_for('list_tasks'))


@app.route('/tasks/<int:task_id>/toggle', methods=['GET'])
def toggle_task(task_id):
    """Toggle task completion"""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break
    return redirect(url_for('list_tasks'))


@app.route('/tasks/<int:task_id>/delete', methods=['GET'])
def delete_task_route(task_id):
    """Delete a task"""
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('list_tasks'))


# ============================================================
# LESSON 5: Integration
# ============================================================

@app.route('/dashboard')
def dashboard():
    """Dashboard showing all info"""
    completed = len([t for t in tasks if t["completed"]])
    return jsonify({
        "total_tasks": len(tasks),
        "completed_tasks": completed,
        "pending_tasks": len(tasks) - completed,
        "message": "Welcome to your Python Dashboard!"
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Page not found"}), 404


# ============================================================
# RUN THE APP
# ============================================================

def run_web_app():
    """Run the Flask web application"""
    print("=" * 50)
    print("🚀 Flask Web Application")
    print("=" * 50)
    print("\nRoutes:")
    print("  GET  /              - Home page")
    print("  GET  /about         - About page")
    print("  GET  /contact       - Contact form")
    print("  POST /submit        - Submit contact form")
    print("  GET  /template-demo - Template example")
    print("  GET  /api/data      - API endpoint")
    print("  GET  /tasks         - Task manager")
    print("  POST /tasks         - Add task")
    print("  GET  /dashboard     - Dashboard")
    print("\nAPI Endpoints:")
    print("  GET    /api/tasks       - List tasks")
    print("  POST   /api/tasks       - Create task")
    print("  PUT    /api/tasks/<id>  - Update task")
    print("  DELETE /api/tasks/<id>  - Delete task")
    print("\n" + "=" * 50)
    print("Starting Flask server on http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    run_web_app()
