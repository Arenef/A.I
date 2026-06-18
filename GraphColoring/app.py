import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
import time
from backtrack import variable, csp
from forward_checking import forward_checking

districts = ["Gò Vấp", "Bình Thạnh", "Phú Nhuận", "Tân Bình", "Quận 1", "Quận 3", "Quận 10", "Quận 11", "Quận 5", "Quận 6", "Quận 4"]

adjacency_dict = {
    "Gò Vấp": ["Tân Bình", "Phú Nhuận", "Bình Thạnh"],
    "Bình Thạnh": ["Gò Vấp", "Phú Nhuận", "Quận 1"],
    "Phú Nhuận": ["Gò Vấp", "Bình Thạnh", "Tân Bình", "Quận 3", "Quận 1"],
    "Tân Bình": ["Gò Vấp", "Phú Nhuận", "Quận 3", "Quận 10", "Quận 11"],
    "Quận 1": ["Bình Thạnh", "Phú Nhuận", "Quận 3", "Quận 5", "Quận 4"],
    "Quận 3": ["Phú Nhuận", "Tân Bình", "Quận 1", "Quận 10", "Quận 5"],
    "Quận 10": ["Tân Bình", "Quận 3", "Quận 11", "Quận 5"],
    "Quận 11": ["Tân Bình", "Quận 10", "Quận 6", "Quận 5"],
    "Quận 5": ["Quận 10", "Quận 3", "Quận 1", "Quận 11", "Quận 6", "Quận 4"],
    "Quận 6": ["Quận 11", "Quận 5"],
    "Quận 4": ["Quận 1", "Quận 5"]
}

color_codes = {
    "red": "#ef4444",     # Soft red
    "green": "#10b981",   # Soft emerald
    "yellow": "#fbbf24",  # Warm yellow
    "cyan": "#06b6d4",    # Sky cyan
    None: "#2a2b3d"       # Gray for unassigned
}


color_map = {
    "Đỏ": "red",
    "Xanh lá": "green",
    "Vàng": "yellow",
    "Xanh dương": "cyan"
}

current_assignment = {d: None for d in districts}


class VisualCSP(csp):
    def __init__(self, variables, callbacks=None):
        super().__init__(variables)
        self.callbacks = callbacks or {}

    def solve(self, i):
        if i == len(self.variables):
            return self.assignment
        
        current_var = self.variables[i]
        
        if 'on_visit' in self.callbacks:
            self.callbacks['on_visit'](current_var.name)
            
        for color in current_var.domains:
            if 'on_try' in self.callbacks:
                self.callbacks['on_try'](current_var.name, color)

            if self.is_valid(current_var, color):
                self.assignment[current_var.name] = color
                
                if 'on_valid' in self.callbacks:
                    self.callbacks['on_valid'](current_var.name, color)
                
                result = self.solve(i + 1)
                if result is not None:
                    return result
            else:
                if 'on_violate' in self.callbacks:
                    self.callbacks['on_violate'](current_var.name, color)
                
            if current_var.name in self.assignment:
                del self.assignment[current_var.name]
                if 'on_backtrack' in self.callbacks:
                    self.callbacks['on_backtrack'](current_var.name)
                
        if 'on_backtrack' in self.callbacks:
            self.callbacks['on_backtrack'](current_var.name)
        return None


class VisualForwardChecking(forward_checking):
    def __init__(self, variables, callbacks=None):
        super().__init__(variables)
        self.callbacks = callbacks or {}

    def remove_domains(self, variable):
        color = self.assignments[variable.name]
        pruned = []
        for i in range(len(self.variables)):
            var = self.variables[i]
            if var.name not in self.assignments and var.name in variable.constraints:
                if color in var.domains:
                    var.domains.remove(color)
                    pruned.append(var)
                    if 'on_fc_prune' in self.callbacks:
                        self.callbacks['on_fc_prune'](var.name, color)
        return pruned

    def add_domains(self, pruned_variables, color):
        for var in pruned_variables:
            if color not in var.domains:
                var.domains.append(color)
                if 'on_fc_restore' in self.callbacks:
                    self.callbacks['on_fc_restore'](var.name, color)

    def solve(self, i):
        if i == len(self.variables):
            return self.assignments
        
        current_var = self.variables[i]
        if 'on_visit' in self.callbacks:
            self.callbacks['on_visit'](current_var.name)
            
        for color in current_var.domains:
            if 'on_try' in self.callbacks:
                self.callbacks['on_try'](current_var.name, color)

            if self.is_valid(current_var, color):
                self.assignments[current_var.name] = color
                
                if 'on_valid' in self.callbacks:
                    self.callbacks['on_valid'](current_var.name, color)
                
                pruned = self.remove_domains(current_var)
                
                any_empty = any(len(var.domains) == 0 for var in self.variables if var.name not in self.assignments)
                
                result = None
                if not any_empty:
                    result = self.solve(i + 1)
                else:
                    if 'on_violate' in self.callbacks:
                        self.callbacks['on_violate'](current_var.name, color)
                
                if result is not None:
                    return result
                
                self.add_domains(pruned, color)
            else:
                if 'on_violate' in self.callbacks:
                    self.callbacks['on_violate'](current_var.name, color)
                
            if current_var.name in self.assignments:
                del self.assignments[current_var.name]
                if 'on_backtrack' in self.callbacks:
                    self.callbacks['on_backtrack'](current_var.name)
                
        if 'on_backtrack' in self.callbacks:
            self.callbacks['on_backtrack'](current_var.name)
        return None


class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring AI")
        self.root.geometry("1300x720")
        self.root.configure(bg="#1e1e2f")

        self.running = False
        self.delay = 0.3  
        self.polygon_ids = {}
        self.map_default_fill = color_codes[None]
        self.stats = {"steps": 0, "backtracks": 0}

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.columnconfigure(0, weight=0, minsize=240)  # Left frame
        self.root.columnconfigure(1, weight=3, minsize=650)  # Center map
        self.root.columnconfigure(2, weight=2, minsize=400)  # Right log
        self.root.rowconfigure(0, weight=0)  # Header
        self.root.rowconfigure(1, weight=1)  # Content

        header_frame = tk.Frame(self.root, bg="#1e1e2f", height=60)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        lbl_header = tk.Label(header_frame, text="🎨 Graph Coloring AI", font=("Segoe UI", 20, "bold"), fg="#ffffff", bg="#1e1e2f")
        lbl_header.pack(pady=10)

        left_panel = tk.Frame(self.root, bg="#242541")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(15, 10), pady=(10, 15))

        lbl_algo_title = tk.Label(left_panel, text="Thuật toán", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#242541")
        lbl_algo_title.pack(pady=(25, 25))
        
        lbl_select = tk.Label(left_panel, text="Chọn thuật toán:", font=("Segoe UI", 10), fg="#b0b0cc", bg="#242541")
        lbl_select.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.algo_var = tk.StringVar(value="Backtracking")
        algos = ["Backtracking", "Forward Checking"]


        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", 
                        fieldbackground="#1e1e2f", 
                        background="#242541", 
                        foreground="white", 
                        darkcolor="#242541", 
                        lightcolor="#242541",
                        selectbackground="#3b82f6")
        
        self.algo_cb = ttk.Combobox(left_panel, textvariable=self.algo_var, values=algos, state="readonly", font=("Segoe UI", 10))
        self.algo_cb.pack(fill="x", padx=20, pady=(0, 15))
        
        self.lbl_group = tk.Label(left_panel, text="Nhóm: CSP / Quay lui", font=("Segoe UI", 9, "italic"), fg="#a29bfe", bg="#242541")
        self.lbl_group.pack(anchor="w", padx=20, pady=(0, 40))

        btn_frame = tk.Frame(left_panel, bg="#242541")
        btn_frame.pack(fill="x", padx=20)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        self.btn_run = tk.Button(btn_frame, text="▶ RUN", font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="#000000", activebackground="#27ae60", activeforeground="#000000", relief="flat", bd=0, cursor="hand2", command=self.start_simulation)
        self.btn_run.grid(row=0, column=0, padx=(0, 5), ipady=8, sticky="ew")
        
        self.btn_reset = tk.Button(btn_frame, text="⟳ RESET", font=("Segoe UI", 10, "bold"), bg="#ff7675", fg="#000000", activebackground="#e17055", activeforeground="#000000", relief="flat", bd=0, cursor="hand2", command=self.reset_map)
        self.btn_reset.grid(row=0, column=1, padx=(5, 0), ipady=8, sticky="ew")

        center_panel = tk.Frame(self.root, bg="#1e1e2f", padx=10)
        center_panel.grid(row=1, column=1, sticky="nsew", pady=(10, 15))

        canvas_card = tk.Frame(center_panel, bg="#242541", bd=0, highlightthickness=1, highlightbackground="#374151")
        canvas_card.pack(fill="both", expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(canvas_card, width=650, height=430, bg="#11111e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)

        self.lbl_status = tk.Label(center_panel, text="Trạng thái: Sẵn sàng", font=("Segoe UI", 12, "bold"), fg="#2ecc71", bg="#1e1e2f")
        self.lbl_status.pack(pady=5)

        style.configure("Custom.Horizontal.TProgressbar", troughcolor='#242541', background='#10b981', thickness=15)
        self.progress = ttk.Progressbar(center_panel, style="Custom.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(5, 10))

        lbl_sol = tk.Label(center_panel, text="Solution Path", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#1e1e2f")
        lbl_sol.pack(anchor="w", pady=(5, 3))
        
        self.solution_area = tk.Text(center_panel, height=2, bg="#11111e", fg="#e5e7eb", font=("Segoe UI", 10), bd=0, highlightthickness=1, highlightbackground="#374151")
        self.solution_area.insert("1.0", "Chưa có")
        self.solution_area.config(state=tk.DISABLED)
        self.solution_area.pack(fill="x")

        right_panel = tk.Frame(self.root, bg="#242541")
        right_panel.grid(row=1, column=2, sticky="nsew", padx=(10, 15), pady=(10, 15))

        lbl_log_title = tk.Label(right_panel, text="Log", font=("Segoe UI", 14, "bold"), fg="#ffffff", bg="#242541")
        lbl_log_title.pack(pady=(20, 15))

        self.log_area = scrolledtext.ScrolledText(right_panel, bg="#11111e", fg="#e5e7eb", font=("Consolas", 10), insertbackground="white", highlightthickness=0, bd=0)
        self.log_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.log_area.tag_config("valid", foreground="#34d399")
        self.log_area.tag_config("violate", foreground="#f87171")
        self.log_area.tag_config("backtrack", foreground="#fbbf24")
        self.log_area.tag_config("fc", foreground="#22d3ee")
        self.log_area.tag_config("header", foreground="#60a5fa", font=("Consolas", 10, "bold"))
        self.log_area.tag_config("info", foreground="#ffffff")

        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        
        coords = {
            "Tân Bình":   [60, 40, 270, 35, 290, 135, 250, 210, 190, 240, 140, 230, 60, 190],
            "Gò Vấp":     [270, 35, 430, 30, 410, 125, 290, 135],
            "Bình Thạnh":  [430, 30, 600, 70, 590, 225, 470, 210, 410, 125],
            "Phú Nhuận":  [290, 135, 410, 125, 470, 210, 380, 265, 250, 210],
            "Quận 11":    [60, 190, 140, 230, 165, 340, 110, 370, 55, 350],
            "Quận 10":    [140, 230, 190, 240, 230, 330, 165, 340],
            "Quận 3":     [250, 210, 380, 265, 350, 340, 230, 330, 190, 240],
            "Quận 1":     [380, 265, 470, 210, 590, 225, 575, 400, 470, 385, 350, 340],
            "Quận 6":     [55, 350, 110, 370, 110, 460, 50, 445],
            "Quận 5":     [110, 370, 165, 340, 230, 330, 350, 340, 470, 385, 430, 475, 110, 460],
            "Quận 4":     [470, 385, 575, 400, 560, 475, 430, 475]
        }

        for d in districts:
            color_key = current_assignment[d]
            color = color_codes[color_key]

            poly_id = self.canvas.create_polygon(coords[d], fill=color, outline="#ffffff", width=2)
            self.polygon_ids[d] = poly_id

            x_coords = coords[d][0::2]
            y_coords = coords[d][1::2]
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)

            text_color = "#11111e" if color_key in [None, "yellow"] else "#ffffff"
            shadow_color = "#ffffff" if text_color == "#11111e" else "#11111e"
            self.canvas.create_text(center_x + 1, center_y + 1, text=d, font=("Segoe UI", 9, "bold"), fill=shadow_color)
            self.canvas.create_text(center_x, center_y, text=d, font=("Segoe UI", 9, "bold"), fill=text_color)


    def log(self, message, tag="info"):
        self.log_area.insert(tk.END, message + "\n", tag)
        self.log_area.see(tk.END)

    def update_status(self, text, color="#2ecc71"):
        self.lbl_status.config(text=f"Trạng thái: {text}", fg=color)

    def update_solution_path(self, text):
        self.solution_area.config(state=tk.NORMAL)
        self.solution_area.delete("1.0", tk.END)
        self.solution_area.insert("1.0", text)
        self.solution_area.config(state=tk.DISABLED)

    def update_progress(self):
        colored_count = sum(1 for d in districts if current_assignment[d] is not None)
        pct = (colored_count / len(districts)) * 100
        self.progress['value'] = pct

    def start_simulation(self):
        if self.running:
            self.stop_simulation()
            return
        
        self.running = True
        self.btn_run.config(text="■ STOP", bg="#ef4444")
        self.update_status("Đang chạy...", "#3b82f6")

        threading.Thread(target=self.run_solvers, daemon=True).start()

    def stop_simulation(self):
        self.running = False
        self.btn_run.config(text="▶ RUN", bg="#2ecc71")
        self.update_status("Đã dừng", "#ef4444")

    def check_control_state(self):
        if not self.running:
            raise InterruptedError("Simulation stopped")

    def reset_map(self):
        if self.running:
            self.stop_simulation()
        for d in districts:
            current_assignment[d] = None
        self.draw_map()
        self.update_progress()
        self.log_area.delete("1.0", tk.END)
        self.update_solution_path("Chưa có")
        self.update_status("Sẵn sàng", "#2ecc71")

    def run_solvers(self):
        self.log_area.delete("1.0", tk.END)
        self.update_solution_path("Đang tính toán...")
        
        for d in districts:
            current_assignment[d] = None
        self.draw_map()
        self.update_progress()
        
        algo = self.algo_var.get()
        self.log(f"=== BẮT ĐẦU CHẠY: {algo.upper()} ===", "header")
        
        try:
            callbacks = {
                'on_visit': self.cb_on_visit,
                'on_try': self.cb_on_try,
                'on_valid': self.cb_on_valid,
                'on_violate': self.cb_on_violate,
                'on_backtrack': self.cb_on_backtrack,
                'on_fc_prune': self.cb_on_fc_prune,
                'on_fc_restore': self.cb_on_fc_restore
            }

            domains = ['Đỏ', 'Xanh lá', 'Vàng', 'Xanh dương']
            variables_list = []
            for name, constraints in adjacency_dict.items():
                variables_list.append(variable(name=name, domains=list(domains), constraints=constraints))
                
            if algo == "Backtracking":
                problem = VisualCSP(variables=variables_list, callbacks=callbacks)
            elif algo == "Forward Checking":
                problem = VisualForwardChecking(variables=variables_list, callbacks=callbacks)
            else:
                self.log(f"[LỖI] Thuật toán '{algo}' không hợp lệ!", "violate")
                return
            
            solution = problem.solve(0)
            success = solution is not None
                
            if success and solution:
                self.log("\n=> ĐÃ TÌM THẤY LỜI GIẢI HỢP LỆ!", "valid")
                self.update_status("Hoàn thành", "#10b981")
                
                res_str = " -> ".join([f"{var_name}: {color}" for var_name, color in solution.items()])
                self.update_solution_path(res_str)
            else:
                self.log("\n=> KHÔNG TÌM THẤY GIẢI PHÁP!", "violate")
                self.update_status("Thất bại", "#ef4444")
                self.update_solution_path("Không tìm thấy lời giải hợp lệ.")
                
        except InterruptedError:
            self.log("\n=> ĐÃ DỪNG MÔ PHỎNG.", "backtrack")
            self.update_status("Đã dừng", "#ef4444")
            self.update_solution_path("Đã dừng mô phỏng.")
        finally:
            self.running = False
            self.btn_run.config(text="▶ RUN", bg="#2ecc71")

    def cb_on_visit(self, var_name):
        self.log(f"\n[Xét quận]: {var_name}", "header")

    def cb_on_try(self, var_name, color_name):
        self.check_control_state()

        tk_color = color_map[color_name]
        current_assignment[var_name] = tk_color
        self.draw_map()
        self.log(f"-> Thử tô màu {color_name}", "info")
        self.update_progress()
        time.sleep(self.delay)

    def cb_on_valid(self, var_name, color_name):
        self.log(f"   [Hợp lệ] {var_name} thỏa mãn ràng buộc.", "valid")

    def cb_on_violate(self, var_name, color_name):
        self.log(f"   [Vi phạm] Trùng màu lân cận!", "violate")

    def cb_on_fc_prune(self, var_name, color_name):
        self.log(f"   [FC] Loại bỏ màu {color_name} khỏi miền của {var_name}", "fc")

    def cb_on_fc_restore(self, var_name, color_name):
        self.log(f"   [FC] Khôi phục màu {color_name} cho miền của {var_name}", "fc")

    def cb_on_backtrack(self, var_name):
        self.check_control_state()
        
        current_assignment[var_name] = None
        self.draw_map()
        self.log(f"<- Quay lui tại: {var_name}", "backtrack")
        self.update_progress()
        time.sleep(self.delay)


    def on_close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringApp(root)
    root.mainloop()
