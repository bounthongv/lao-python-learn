# Phase 2: Tkinter Desktop Application

"""
Phase 2: Simple Desktop Application with Tkinter
Learning Objectives:
- GUI fundamentals with Tkinter
- Widget creation and layout
- Event handling
- Building a complete desktop app
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

# ============================================================
# LESSON 1: Creating a Window
# ============================================================

def lesson1_create_window():
    """Create a basic Tkinter window"""
    # Create main window
    root = tk.Tk()
    root.title("My First Window - Lesson 1")
    root.geometry("400x300")
    
    # Add a label
    label = tk.Label(root, text="Hello from Tkinter!", font=("Arial", 16))
    label.pack(pady=20)
    
    # Run the app
    root.mainloop()


# ============================================================
# LESSON 2: Widgets and Layouts
# ============================================================

def lesson2_widgets():
    """Create widgets and layouts"""
    root = tk.Tk()
    root.title("Widgets Example - Lesson 2")
    root.geometry("500x400")
    
    # Frame for organization
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Button
    btn = tk.Button(frame, text="Click Me!", command=lambda: messagebox.showinfo("Info", "Button clicked!"))
    btn.pack(pady=10)
    
    # Entry (text input)
    entry = tk.Entry(frame, width=30)
    entry.pack(pady=5)
    
    # Text area
    text = tk.Text(frame, height=5, width=40)
    text.pack(pady=10)
    text.insert("1.0", "Type something here...")
    
    # Checkbuttons
    var1 = tk.BooleanVar()
    cb1 = tk.Checkbutton(frame, text="Option 1", variable=var1)
    cb1.pack()
    
    # Radio buttons
    var = tk.StringVar(value="A")
    rb1 = tk.Radiobutton(frame, text="Option A", variable=var, value="A")
    rb2 = tk.Radiobutton(frame, text="Option B", variable=var, value="B")
    rb1.pack()
    rb2.pack()
    
    root.mainloop()


# ============================================================
# LESSON 3: Event Handling
# ============================================================

def lesson3_events():
    """Handle events and user interactions"""
    root = tk.Tk()
    root.title("Event Handling - Lesson 3")
    root.geometry("400x300")
    
    counter = [0]  # Use list to allow modification in nested function
    
    def increment():
        counter[0] += 1
        label.config(text=f"Count: {counter[0]}")
    
    def reset():
        counter[0] = 0
        label.config(text=f"Count: {counter[0]}")
    
    # Label to display counter
    label = tk.Label(root, text="Count: 0", font=("Arial", 24))
    label.pack(pady=30)
    
    # Buttons
    btn_inc = tk.Button(root, text="Increment", command=increment, width=15)
    btn_inc.pack(pady=5)
    
    btn_reset = tk.Button(root, text="Reset", command=reset, width=15)
    btn_reset.pack(pady=5)
    
    # Keyboard binding
    root.bind("<Return>", lambda e: increment())
    root.bind("<Escape>", lambda e: reset())
    
    root.mainloop()


# ============================================================
# LESSON 4: Building a Complete App - To-Do List
# ============================================================

class TodoApp:
    """Complete To-Do List Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List - Lesson 4")
        self.root.geometry("500x400")
        
        # Task list
        self.tasks = []
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title = tk.Label(self.root, text="My To-Do List", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        self.task_entry = tk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        
        # Listbox to show tasks
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.task_listbox = tk.Listbox(list_frame, height=15, width=50)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        
        # Button frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        """Add a new task"""
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_listbox.insert(tk.END, f"☐ {task}")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def complete_task(self):
        """Mark a task as completed"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["completed"] = True
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, f"☑ {self.tasks[index]['task']}")
    
    def delete_task(self):
        """Delete a selected task"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks.pop(index)
            self.task_listbox.delete(index)
    
    def clear_all(self):
        """Clear all tasks"""
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks.clear()
            self.task_listbox.delete(0, tk.END)


def lesson4_todo_app():
    """Run the To-Do List application"""
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


# ============================================================
# LESSON 5: OOP and Classes
# ============================================================

class Calculator:
    """Simple Calculator Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator - Lesson 5")
        self.root.geometry("300x400")
        
        self.expression = ""
        self.result = 0
        
        # Display
        self.display = tk.Entry(root, font=("Arial", 20), justify=tk.RIGHT)
        self.display.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Button grid
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        ]
        
        row = 0
        col = 0
        for btn in buttons:
            command = lambda b=btn: self.on_button_click(b)
            button = tk.Button(root, text=btn, font=("Arial", 16), width=5, height=2, command=command)
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def on_button_click(self, char):
        """Handle button clicks"""
        if char == "C":
            self.display.delete(0, tk.END)
            self.expression = ""
        elif char == "=":
            try:
                result = eval(self.expression)
                self.display.insert(tk.END, f" = {result}")
                self.expression = str(result)
            except:
                self.display.insert(tk.END, " Error")
                self.expression = ""
        else:
            self.display.insert(tk.END, char)
            self.expression += char


def lesson5_calculator():
    """Run the Calculator application"""
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    """Display main menu for all lessons"""
    root = tk.Tk()
    root.title("Lao Python Learning - Desktop Apps")
    root.geometry("500x400")
    
    # Title
    title = tk.Label(root, text="🐍 Desktop Application Lessons", 
                     font=("Arial", 16, "bold"))
    title.pack(pady=20)
    
    # Menu items
    lessons = [
        ("Lesson 1: Creating a Window", lesson1_create_window),
        ("Lesson 2: Widgets and Layouts", lesson2_widgets),
        ("Lesson 3: Event Handling", lesson3_events),
        ("Lesson 4: To-Do List App", lesson4_todo_app),
        ("Lesson 5: Calculator App", lesson5_calculator),
    ]
    
    for text, command in lessons:
        btn = tk.Button(root, text=text, font=("Arial", 12), 
                       width=35, height=2, command=command)
        btn.pack(pady=5)
    
    root.mainloop()


if __name__ == "__main__":
    main_menu()
