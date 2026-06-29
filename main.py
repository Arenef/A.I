import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Artificial Intelligence - Main Menu")
        self.root.geometry("600x450")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(
            self.root,
            text="AI Mode",
            bg="#1e1e2e",
            fg="white",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=(30, 10))

        subtitle = tk.Label(
            self.root,
            text="Vui lòng chọn chế độ (Select Mode)",
            bg="#1e1e2e",
            fg="#cdd6f4",
            font=("Segoe UI", 14)
        )
        subtitle.pack(pady=(0, 30))

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=60)

        self.create_button(btn_frame, "🤖 Máy hút bụi (Vacuum Cleaner)", "#89b4fa", self.run_vacuum)
        self.create_button(btn_frame, "🎨 Tô màu đồ thị (Graph Coloring)", "#a6e3a1", self.run_graph_coloring)
        self.create_button(btn_frame, "⭕ Cờ Caro (Tic-Tac-Toe)", "#f38ba8", self.run_tictactoe)

    def create_button(self, parent, text, color, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 14, "bold"),
            bg=color,
            fg="#11111b",
            activebackground="#cdd6f4",
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=15,
            command=command
        )
        btn.pack(fill="x", pady=10)

        # Hover effects
        def on_enter(e):
            btn.config(bg="#cdd6f4")

        def on_leave(e):
            btn.config(bg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def run_app(self, folder, filename):
        # Hide the main window
        self.root.withdraw()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_dir, folder, filename)
        
        # Run the app in its own directory so imports work correctly
        try:
            subprocess.run([sys.executable, app_path], cwd=os.path.join(script_dir, folder))
        except Exception as e:
            print(f"Error running {filename}: {e}")
            
        # Show the main window again when the app is closed
        self.root.deiconify()

    def run_vacuum(self):
        self.run_app("AppVaccum", "app.py")

    def run_graph_coloring(self):
        self.run_app("GraphColoring", "app.py")

    def run_tictactoe(self):
        self.run_app("TicTacToe", "app.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
