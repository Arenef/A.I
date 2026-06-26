import tkinter as tk
from tkinter import ttk

from dfs_vacuum_1 import dfs_vacuum_1
from dfs_vacuum_2 import dfs_vacuum_2
from bfs_vaccum_1 import bfs_vacuum_1
from bfs_vaccum_2 import bfs_vacuum_2
from ucs_vacuum import ucs_vacuum
from a_star_vacuum import a_star_vacuum
from greedy_vacuum import greedy_vacuum
from ida_star import ida_star_vacuum
from simple_hill_climb import simple_hill_climb_vacuum
from steepest_ascent_hill_climbing import steepest_ascent_hill_climbing
from stochastic_hill_climbing import stochastic_ascent_hill_climbing
from local_beam_search import local_beam_search
from random_restart_hill_climbing import random_restart_hill_climbing
from simulated_annealing import simulated_annealing
from ids_vacuum import ids_vacuum
from and_or_search_vacuum import and_or_search_vacuum
from partially_observable_vacuum import partially_observable_vacuum
from belief_state_search_vacuum import belief_state_search_vacuum

class VacuumApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Vacuum Cleaner AI")

        self.root.geometry("1100x750")

        self.root.configure(bg="#1e1e2e")

        self.vaccum_logic = None

        self.path = []

        self.step_idx = 0

        self.is_running = False

        self.search_path = []

        self.solution_path = []

        self.solution_idx = 0

        self.animation_phase = "search"

        self.speed_var = tk.IntVar()
        self.speed_var.set(500)

        self.setup_style()

        self.setup_ui()

        self.load_algorithm()

        self.draw_grid(
            self.vaccum_logic.start
        )

    def setup_style(self):

        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        self.style.configure(
            "TCombobox",
            font=("Segoe UI", 10),
            fieldbackground="#181825",
            background="#313244",
            foreground="white",
            arrowcolor="white",
            bordercolor="#45475a"
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#181825")],
            foreground=[("readonly", "white")]
        )

    def setup_ui(self):

        title = tk.Label(
            self.root,
            text="🤖 Vacuum Cleaner AI",
            bg="#1e1e2e",
            fg="white",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(pady=10)

        main_frame = tk.Frame(
            self.root,
            bg="#1e1e2e"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        self.left_frame = tk.Frame(
            main_frame,
            bg="#313244",
            width=300
        )

        self.left_frame.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        tk.Label(
            self.left_frame,
            text="Điều khiển",
            bg="#313244",
            fg="white",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(15, 5))

        btn_frame = tk.Frame(
            self.left_frame,
            bg="#313244"
        )
        btn_frame.pack(
            pady=10,
            padx=15,
            fill="x"
        )

        self.run_btn = tk.Button(
            btn_frame,
            text="▶ RUN",
            command=self.run_algorithm,
            font=("Segoe UI", 9, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )
        self.run_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 2)
        )

        def on_enter_run(e):
            self.run_btn.config(bg="#89b4fa", fg="#11111b")

        def on_leave_run(e):
            self.run_btn.config(bg="#a6e3a1", fg="#11111b")

        self.run_btn.bind("<Enter>", on_enter_run)
        self.run_btn.bind("<Leave>", on_leave_run)

        self.show_path_btn = tk.Button(
            btn_frame,
            text="▶ SHOW PATH",
            command=self.run_solution_only,
            font=("Segoe UI", 9, "bold"),
            bg="#f9e2af",
            fg="#11111b",
            activebackground="#eba0ac",
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )
        self.show_path_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(2, 2)
        )

        def on_enter_show_path(e):
            self.show_path_btn.config(bg="#f2cdcd", fg="#11111b")

        def on_leave_show_path(e):
            self.show_path_btn.config(bg="#f9e2af", fg="#11111b")

        self.show_path_btn.bind("<Enter>", on_enter_show_path)
        self.show_path_btn.bind("<Leave>", on_leave_show_path)

        self.reset_btn = tk.Button(
            btn_frame,
            text="⟳ RESET",
            command=self.reset_app,
            font=("Segoe UI", 9, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            activebackground="#eba0ac",
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10
        )
        self.reset_btn.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(2, 0)
        )

        def on_enter_reset(e):
            self.reset_btn.config(bg="#eba0ac", fg="#11111b")

        def on_leave_reset(e):
            self.reset_btn.config(bg="#f38ba8", fg="#11111b")

        self.reset_btn.bind("<Enter>", on_enter_reset)
        self.reset_btn.bind("<Leave>", on_leave_reset)

        speed_frame = tk.Frame(
            self.left_frame,
            bg="#313244"
        )
        speed_frame.pack(
            pady=10,
            padx=15,
            fill="x"
        )

        self.speed_label = tk.Label(
            speed_frame,
            text="Tốc độ: 500 ms",
            bg="#313244",
            fg="white",
            font=("Segoe UI", 10, "bold")
        )
        self.speed_label.pack(anchor="w", pady=(0, 5))

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=50,
            to=2000,
            orient="horizontal",
            variable=self.speed_var,
            bg="#313244",
            fg="white",
            troughcolor="#181825",
            activebackground="#cba6f7",
            highlightthickness=0,
            bd=0,
            showvalue=False,
            command=self.update_speed_label
        )
        self.speed_scale.pack(fill="x")

        tk.Label(
            self.left_frame,
            text="Thuật toán",
            bg="#313244",
            fg="white",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(20, 5))

        self.category_var = tk.StringVar()
        self.category_var.set("Uninformed Search")

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("DFS 1")

        self.algo_categories = {
            "Uninformed Search": ["DFS 1", "DFS 2", "BFS 1", "BFS 2", "UCS", "IDS"],
            "Informed Search": ["Greedy", "A*", "IDA*"],
            "Local Search": ["Simple Hill Climb", "Steepest Ascent Hill Climbing", "Stochastic Ascent Hill Climbing", 
                            "Random Restart Hill Climbing", "Local Beam Search", "Simulated Annealing"],
            "Complex Environment": ["AND-OR Search", "Partially Observable Vacuum", "Belief State Search"]
        }

        tk.Label(
            self.left_frame,
            text="Nhóm thuật toán:",
            bg="#313244",
            fg="#cba6f7",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=15, pady=(5, 2))

        self.cat_combobox = ttk.Combobox(
            self.left_frame,
            textvariable=self.category_var,
            values=list(self.algo_categories.keys()),
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.cat_combobox.pack(fill="x", padx=15, pady=(0, 10))
        self.cat_combobox.bind("<<ComboboxSelected>>", self.on_category_changed)

        tk.Label(
            self.left_frame,
            text="Thuật toán:",
            bg="#313244",
            fg="#cba6f7",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=15, pady=(5, 2))

        self.algo_combobox = ttk.Combobox(
            self.left_frame,
            textvariable=self.algorithm_var,
            values=self.algo_categories["Uninformed Search"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.algo_combobox.pack(fill="x", padx=15, pady=(0, 10))
        self.algo_combobox.bind("<<ComboboxSelected>>", self.on_algo_changed)

        self.center_frame = tk.Frame(
            main_frame,
            bg="#1e1e2e"
        )

        self.center_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            self.center_frame,
            width=500,
            height=500,
            bg="#181825",
            highlightthickness=0
        )

        self.canvas.pack(pady=20)

        self.status_label = tk.Label(
            self.center_frame,
            text="Trạng thái: Sẵn sàng",
            bg="#1e1e2e",
            fg="#a6e3a1",
            font=("Segoe UI", 12, "bold")
        )

        self.status_label.pack()

        self.progress = ttk.Progressbar(
            self.center_frame,
            length=400,
            mode="determinate"
        )

        self.progress.pack(pady=15)

        solution_frame = tk.Frame(
            self.center_frame,
            bg="#1e1e2e"
        )

        solution_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            solution_frame,
            text="Solution Path",
            bg="#1e1e2e",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        solution_container = tk.Frame(
            solution_frame,
            bg="#313244",
            height=60
        )

        solution_container.pack(
            fill="x",
            pady=5
        )

        self.solution_scroll = tk.Scrollbar(
            solution_container,
            orient="horizontal"
        )

        self.solution_scroll.pack(
            side="bottom",
            fill="x"
        )

        self.solution_canvas = tk.Canvas(
            solution_container,
            bg="#181825",
            height=50,
            width=500,
            highlightthickness=0,
            xscrollcommand=self.solution_scroll.set
        )

        self.solution_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.solution_scroll.config(
            command=self.solution_canvas.xview
        )

        self.solution_text = self.solution_canvas.create_text(
            10,
            22,
            anchor="w",
            text="Chưa có",
            fill="#89b4fa",
            font=("Consolas", 11, "bold")
        )

        self.right_frame = tk.Frame(
            main_frame,
            bg="#313244",
            width=250
        )

        self.right_frame.pack(
            side="right",
            fill="y",
            padx=10,
            pady=10
        )

        tk.Label(
            self.right_frame,
            text="Log",
            bg="#313244",
            fg="white",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=10)

        self.log_text = tk.Text(
            self.right_frame,
            bg="#181825",
            fg="white",
            font=("Consolas", 10)
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def update_speed_label(self, val):
        self.speed_label.config(text=f"Tốc độ: {val} ms")

    def get_speed(self):
        try:
            val = self.speed_var.get()
            if val < 10:
                val = 10
            return val
        except (tk.TclError, ValueError):
            return 500

    def on_algo_changed(self, event=None):
        self.load_algorithm()
        if self.vaccum_logic:
            self.draw_grid(self.vaccum_logic.start)
            self.status_label.config(text="Trạng thái: Sẵn sàng")
            self.progress["value"] = 0
            self.solution_canvas.itemconfig(self.solution_text, text="Chưa có")
            self.solution_canvas.config(scrollregion=(0, 0, 0, 0))

    def on_category_changed(self, event=None):
        cat = self.category_var.get()
        algos = self.algo_categories.get(cat, [])
        self.algo_combobox.config(values=algos)
        if algos:
            self.algorithm_var.set(algos[0])
            self.on_algo_changed()

    def load_algorithm(self):

        selected = self.algorithm_var.get()

        print("Selected:", selected)

        algorithms = {
            "DFS 1": dfs_vacuum_1,
            "DFS 2": dfs_vacuum_2,
            "BFS 1": bfs_vacuum_1,
            "BFS 2": bfs_vacuum_2,
            "UCS": ucs_vacuum,
            "IDS": ids_vacuum,
            "Greedy": greedy_vacuum,
            "A*": a_star_vacuum,
            "IDA*": ida_star_vacuum,
            "Simple Hill Climb": simple_hill_climb_vacuum,
            "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing,
            "Stochastic Ascent Hill Climbing": stochastic_ascent_hill_climbing,
            "Random Restart Hill Climbing": random_restart_hill_climbing,
            "Local Beam Search": local_beam_search,
            "Simulated Annealing": simulated_annealing,
            "AND-OR Search": and_or_search_vacuum,
            "Partially Observable Vacuum": partially_observable_vacuum,
            "Belief State Search": belief_state_search_vacuum
        }

        self.vaccum_logic = algorithms[selected]()

        print(self.vaccum_logic.start)

    def draw_grid(self, matrix):

        self.canvas.delete("all")

        is_belief = False
        if isinstance(matrix, (list, tuple)) and len(matrix) > 0:
            if isinstance(matrix[0], (list, tuple)) and len(matrix[0]) > 0:
                if isinstance(matrix[0][0], (list, tuple)):
                    is_belief = True

        if is_belief:
            rows = len(matrix[0])
            cols = len(matrix[0][0])
        else:
            rows = len(matrix)
            cols = len(matrix[0])

        cell_size = 500 // cols

        for i in range(rows):

            for j in range(cols):

                x1 = j * cell_size
                y1 = i * cell_size

                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if is_belief:
                    values = {state[i][j] for state in matrix}
                else:
                    values = {matrix[i][j]}

                color = "#cdd6f4"
                text_emoji = ""

                if -1 in values:
                    color = "#45475a"
                    text_emoji = "⬛"
                elif 2 in values:
                    if is_belief:
                        color = "#cba6f7"
                        text_emoji = "🤖" if len(values) == 1 else "🤖?"
                    else:
                        color = "#f38ba8"
                        text_emoji = "🤖"
                elif 1 in values:
                    color = "#f9e2af"
                    if is_belief:
                        text_emoji = "🟤" if len(values) == 1 else "🟤?"
                    else:
                        text_emoji = "🟤"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#11111b",
                    width=3
                )

                if text_emoji:
                    font_size = 24 if "?" in text_emoji else 28
                    self.canvas.create_text(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        text=text_emoji,
                        font=("Arial", font_size)
                    )

    def log(self, message):

        self.log_text.insert(
            tk.END,
            message + "\n"
        )

        self.log_text.see(tk.END)

    def analyze_matrix(self, matrix):
        is_belief = False
        if isinstance(matrix, (list, tuple)) and len(matrix) > 0:
            if isinstance(matrix[0], (list, tuple)) and len(matrix[0]) > 0:
                if isinstance(matrix[0][0], (list, tuple)):
                    is_belief = True

        if is_belief:
            robot_positions = set()
            dirt_positions = set()
            for state in matrix:
                for i in range(len(state)):
                    for j in range(len(state[0])):
                        if state[i][j] == 2:
                            robot_positions.add((i, j))
                        elif state[i][j] == 1:
                            dirt_positions.add((i, j))
            r_pos = sorted(list(robot_positions))
            if len(r_pos) == 1:
                r_pos = r_pos[0]
            return r_pos, len(dirt_positions)
        else:
            robot_pos = (0, 0)
            dirt_count = 0
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 2:
                        robot_pos = (i, j)
                    elif matrix[i][j] == 1:
                        dirt_count += 1
            return robot_pos, dirt_count

    def run_algorithm(self):

        if self.is_running:
            return

        self.load_algorithm()

        if self.vaccum_logic is None:
            return

        self.status_label.config(
            text=f"Đang chạy {self.algorithm_var.get()}"
        )

        node = self.vaccum_logic.solve()

        self.log_text.delete("1.0", tk.END)

        self.log(f"🤖 [KHỞI CHẠY] Thuật toán: {self.algorithm_var.get()}")
        self.log("-" * 35)
        self.log("🔍 QUÁ TRÌNH TÌM KIẾM (FRONTIER - TỪNG BƯỚC):")

        if node is not None:
            path = self.vaccum_logic.get_path(node)
            actions = [
                step[1]
                for step in path
                if step[1] != "START"
            ]
            solution = "  ➜  ".join(actions)
            self.solution_path = path
        else:
            solution = "Không tìm thấy lời giải"
            self.solution_path = []

        self.solution_canvas.itemconfig(
            self.solution_text,
            text=solution
        )

        self.solution_canvas.update_idletasks()

        bbox = self.solution_canvas.bbox(self.solution_text)

        if bbox:
            self.solution_canvas.config(
                scrollregion=bbox
            )

        self.search_path = getattr(self.vaccum_logic, 'search_events', [])
        
        self.progress["maximum"] = len(self.search_path) + len(self.solution_path)
        self.progress["value"] = 0
        self.step_idx = 0
        self.solution_idx = 0
        self.animation_phase = "search"
        self.is_running = True
        self.animate_step()

    def run_solution_only(self):

        if self.is_running:
            return

        self.load_algorithm()

        if self.vaccum_logic is None:
            return

        self.status_label.config(
            text=f"Chạy lời giải {self.algorithm_var.get()}"
        )

        node = self.vaccum_logic.solve()

        self.log_text.delete("1.0", tk.END)

        self.log(f"🤖 [KHỞI CHẠY] Chỉ chạy lời giải: {self.algorithm_var.get()}")
        self.log("-" * 35)

        if node is not None:
            path = self.vaccum_logic.get_path(node)
            actions = [
                step[1]
                for step in path
                if step[1] != "START"
            ]
            solution = "  ➜  ".join(actions)
            self.solution_path = path
        else:
            solution = "Không tìm thấy lời giải"
            self.solution_path = []

        self.solution_canvas.itemconfig(
            self.solution_text,
            text=solution
        )

        self.solution_canvas.update_idletasks()

        bbox = self.solution_canvas.bbox(self.solution_text)

        if bbox:
            self.solution_canvas.config(
                scrollregion=bbox
            )

        self.search_path = []
        
        self.progress["maximum"] = len(self.solution_path)
        self.progress["value"] = 0
        self.step_idx = 0
        self.solution_idx = 0
        
        if self.solution_path:
            self.log("🐾 BẮT ĐẦU DI CHUYỂN THEO LỜI GIẢI (SOLUTION PATH):")
            self.log("-" * 35)
            self.animation_phase = "solution"
            self.is_running = True
            self.animate_step()
        else:
            self.status_label.config(
                text="✔ Hoàn thành"
            )
            self.log("🏆 [HOÀN THÀNH] Không có lời giải để hiển thị.")
            self.log("=" * 35)

    def animate_step(self):

        if self.animation_phase == "search":
            if self.step_idx < len(self.search_path):
                matrix, log_message = self.search_path[self.step_idx]

                self.draw_grid(matrix)
                self.log(log_message)
                self.log("-" * 35)

                self.progress["value"] = self.step_idx + 1
                self.step_idx += 1

                self.root.after(
                    self.get_speed(),
                    self.animate_step
                )
            else:
                if self.solution_path:
                    self.log("🐾 BẮT ĐẦU DI CHUYỂN THEO LỜI GIẢI (SOLUTION PATH):")
                    self.log("-" * 35)
                    self.animation_phase = "solution"
                    self.solution_idx = 0
                    self.root.after(
                        self.get_speed(),
                        self.animate_step
                    )
                else:
                    self.status_label.config(
                        text="✔ Hoàn thành"
                    )
                    self.log("🏆 [HOÀN THÀNH] Hoàn thành quá trình duyệt tìm kiếm! Không tìm thấy lời giải.")
                    self.log("=" * 35)
                    self.is_running = False

        elif self.animation_phase == "solution":
            if self.solution_idx < len(self.solution_path):
                matrix, action = self.solution_path[self.solution_idx]

                self.draw_grid(matrix)
                r_pos, dirt_count = self.analyze_matrix(matrix)
                if action == "START":
                    log_message = f"🤖 Bắt đầu hành trình tại: Vị trí {r_pos} (Số vết bẩn ban đầu: {dirt_count})"
                else:
                    log_message = f"🐾 Bước {self.solution_idx}: Thực hiện hành động '{action}' -> Vị trí {r_pos} (Còn lại {dirt_count} vết bẩn)"
                
                self.log(log_message)
                self.log("-" * 35)

                self.progress["value"] = len(self.search_path) + self.solution_idx + 1
                self.solution_idx += 1

                self.root.after(
                    self.get_speed(),
                    self.animate_step
                )
            else:
                self.status_label.config(
                    text="✔ Hoàn thành"
                )
                self.log("🏆 [HOÀN THÀNH] Robot đã hoàn thành di chuyển dọn dẹp theo lời giải!")
                self.log("=" * 35)
                self.is_running = False

    def reset_app(self):

        self.is_running = False

        self.path = []
        self.search_path = []
        self.solution_path = []
        self.step_idx = 0
        self.solution_idx = 0
        self.animation_phase = "search"

        self.log_text.delete(
            "1.0",
            tk.END
        )

        self.solution_canvas.itemconfig(
            self.solution_text,
            text="Chưa có"
        )

        self.solution_canvas.config(
            scrollregion=(0, 0, 0, 0)
        )

        self.progress["value"] = 0

        self.status_label.config(
            text="Trạng thái: Sẵn sàng"
        )

        self.load_algorithm()

        if self.vaccum_logic:

            self.draw_grid(
                self.vaccum_logic.start
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = VacuumApp(root)

    root.mainloop()
