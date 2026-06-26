import tkinter as tk
from tkinter import font as tkfont
import time
import minimax
import alpha_beta
import expectimax

# Modern Color Palette (Catppuccin Mocha inspired)
BG_MAIN = "#1E1E2E"          # Deep dark background
BG_CARD = "#252538"          # Slightly lighter container bg
COLOR_GRID = "#313244"       # Button grid color
COLOR_HOVER = "#45475A"      # Hover state for grid
COLOR_X = "#F38BA8"          # Warm pastel red for X
COLOR_O = "#89B4FA"          # Pastel blue for O
COLOR_TEXT = "#CDD6F4"       # Off-white text
COLOR_MUTED = "#A6ADC8"      # Muted text
COLOR_WIN = "#A6E3A1"        # Pastel green for winning path
COLOR_WIN_TEXT = "#11111B"   # Dark text for winning cells
COLOR_BTN = "#89B4FA"        # Main action button color
COLOR_BTN_HOVER = "#B4BEFE"  # Main action button hover

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI - Comparison Mode")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)

        # Game State Variables
        self.human_player = "X"      # Human default
        self.ai_player = "O"         # AI default
        self.current_turn = "X"      # 'X' always starts
        self.board = [""] * 9
        self.game_over = False
        self.buttons = []
        self.ai_thinking = False     # Guard to prevent clicks during AI's turn
        self.animation_after_id = None # Track active playback timer
        self.thinking_steps = []
        self.current_step_index = 0

        # Animation Settings
        self.skip_animation = tk.BooleanVar(value=False)
        self.animation_speed = tk.IntVar(value=150)
        
        # AI Algorithm Variable
        self.selected_algo = "alpha_beta"  # "alpha_beta" or "minimax"

        self.setup_fonts()
        self.create_widgets()
        
        # Start game logic
        self.reset_game()

    def setup_fonts(self):
        """Sets up consistent modern fonts."""
        self.title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=10, weight="normal")
        self.status_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.symbol_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.ui_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

    def create_widgets(self):
        """Creates the GUI layout."""
        # Split root into left (game) and right (logs & thinking board) panes
        self.left_pane = tk.Frame(self.root, bg=BG_MAIN, width=420)
        self.left_pane.pack(side="left", fill="both")
        self.left_pane.pack_propagate(False)

        self.right_pane = tk.Frame(self.root, bg=BG_MAIN)
        self.right_pane.pack(side="right", fill="both", expand=True)

        # Top Padding
        tk.Frame(self.left_pane, height=10, bg=BG_MAIN).pack()

        # Header Frame
        header_frame = tk.Frame(self.left_pane, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=25)
        
        title_label = tk.Label(header_frame, text="TIC - TAC - TOE AI", font=self.title_font, fg=COLOR_TEXT, bg=BG_MAIN)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Minimax vs. Alpha-Beta Performance Analyzer", font=self.subtitle_font, fg=COLOR_MUTED, bg=BG_MAIN)
        subtitle_label.pack(pady=(0, 5))

        # Role Selector Frame
        selector_frame = tk.Frame(self.left_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        selector_frame.pack(fill="x", padx=30, pady=5)
        
        role_label = tk.Label(selector_frame, text="Play as:", font=self.ui_font, fg=COLOR_TEXT, bg=BG_CARD)
        role_label.pack(side="left", padx=(15, 10), pady=8)

        self.btn_select_x = tk.Button(
            selector_frame, text="X (First)", font=self.ui_font, bg=COLOR_GRID, fg=COLOR_X,
            activebackground=COLOR_HOVER, activeforeground=COLOR_X, relief="flat", bd=0,
            padx=15, pady=4, cursor="hand2", command=lambda: self.change_role("X")
        )
        self.btn_select_x.pack(side="left", padx=5)

        self.btn_select_o = tk.Button(
            selector_frame, text="O (Second)", font=self.ui_font, bg=COLOR_GRID, fg=COLOR_O,
            activebackground=COLOR_HOVER, activeforeground=COLOR_O, relief="flat", bd=0,
            padx=15, pady=4, cursor="hand2", command=lambda: self.change_role("O")
        )
        self.btn_select_o.pack(side="left", padx=5)

        # Algorithm Selector Frame
        algo_frame = tk.Frame(self.left_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        algo_frame.pack(fill="x", padx=30, pady=5)
        
        algo_label = tk.Label(algo_frame, text="AI Engine:", font=self.ui_font, fg=COLOR_TEXT, bg=BG_CARD)
        algo_label.pack(side="left", padx=(10, 5), pady=8)

        self.btn_algo_minimax = tk.Button(
            algo_frame, text="Minimax", font=self.ui_font, bg=COLOR_GRID, fg=COLOR_TEXT,
            activebackground=COLOR_HOVER, activeforeground=COLOR_TEXT, relief="flat", bd=0,
            padx=8, pady=4, cursor="hand2", command=lambda: self.change_algo("minimax")
        )
        self.btn_algo_minimax.pack(side="left", padx=3)

        self.btn_algo_alphabeta = tk.Button(
            algo_frame, text="Alpha-Beta", font=self.ui_font, bg=COLOR_GRID, fg=COLOR_TEXT,
            activebackground=COLOR_HOVER, activeforeground=COLOR_TEXT, relief="flat", bd=0,
            padx=8, pady=4, cursor="hand2", command=lambda: self.change_algo("alpha_beta")
        )
        self.btn_algo_alphabeta.pack(side="left", padx=3)

        self.btn_algo_expectimax = tk.Button(
            algo_frame, text="Expectimax", font=self.ui_font, bg=COLOR_GRID, fg=COLOR_TEXT,
            activebackground=COLOR_HOVER, activeforeground=COLOR_TEXT, relief="flat", bd=0,
            padx=8, pady=4, cursor="hand2", command=lambda: self.change_algo("expectimax")
        )
        self.btn_algo_expectimax.pack(side="left", padx=3)

        # Status Label
        self.status_label = tk.Label(self.left_pane, text="Your Turn (X)", font=self.status_font, fg=COLOR_TEXT, bg=BG_MAIN)
        self.status_label.pack(pady=5)

        # Grid Container
        grid_container = tk.Frame(self.left_pane, bg=BG_CARD, padx=8, pady=8, highlightthickness=1, highlightbackground=COLOR_GRID)
        grid_container.pack(padx=30, pady=5)

        # 3x3 Grid
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = tk.Button(
                grid_container, text="", font=self.symbol_font, bg=COLOR_GRID, fg=COLOR_TEXT,
                activebackground=COLOR_GRID, activeforeground=COLOR_TEXT, relief="flat", bd=0,
                width=4, height=1, cursor="hand2",
                command=lambda index=i: self.on_cell_click(index)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            # Bind hover events
            btn.bind("<Enter>", lambda e, b=btn: self.on_btn_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_btn_leave(e, b))
            
            self.buttons.append(btn)

        # Metrics Panel (Bảng thông số AI)
        metrics_panel = tk.Frame(self.left_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        metrics_panel.pack(fill="x", padx=30, pady=5)

        metrics_title = tk.Label(metrics_panel, text="AI SEARCH STATS / THÔNG SỐ AI", font=self.ui_font, fg=COLOR_MUTED, bg=BG_CARD)
        metrics_title.pack(anchor="w", padx=15, pady=(6, 2))

        self.lbl_nodes = tk.Label(metrics_panel, text="States Explored (Trạng thái duyệt): -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_nodes.pack(anchor="w", padx=15, pady=1)

        self.lbl_cuts = tk.Label(metrics_panel, text="Pruning Cuts (Lần cắt tỉa): -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_cuts.pack(anchor="w", padx=15, pady=1)

        self.lbl_time = tk.Label(metrics_panel, text="Calculation Time (Thời gian chạy): -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_time.pack(anchor="w", padx=15, pady=(1, 6))

        # Bottom Frame for control buttons
        bottom_frame = tk.Frame(self.left_pane, bg=BG_MAIN)
        bottom_frame.pack(fill="x", padx=30, pady=5)

        self.btn_restart = tk.Button(
            bottom_frame, text="Restart Match", font=self.ui_font, bg=COLOR_BTN, fg=BG_MAIN,
            activebackground=COLOR_BTN_HOVER, activeforeground=BG_MAIN, relief="flat", bd=0,
            padx=20, pady=6, cursor="hand2", command=self.reset_game
        )
        self.btn_restart.pack()
        
        # Hover effect for restart button
        self.btn_restart.bind("<Enter>", lambda e: self.btn_restart.config(bg=COLOR_BTN_HOVER))
        self.btn_restart.bind("<Leave>", lambda e: self.btn_restart.config(bg=COLOR_BTN))

        # Middle Column (Thinking Log Panel)
        self.log_pane = tk.Frame(self.right_pane, bg=BG_MAIN)
        self.log_pane.pack(side="left", fill="both", expand=True)

        log_panel = tk.Frame(self.log_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        log_panel.pack(fill="both", expand=True, padx=(10, 10), pady=(10, 20))

        log_title = tk.Label(log_panel, text="AI THINKING LOGS / TIẾN TRÌNH SUY NGHĨ", font=self.ui_font, fg=COLOR_MUTED, bg=BG_CARD)
        log_title.pack(anchor="w", padx=15, pady=(6, 4))

        # Scrollable text widget for terminal
        self.txt_log = tk.Text(
            log_panel, font=("Consolas", 9), bg="#11111B", fg=COLOR_TEXT,
            relief="flat", bd=0, wrap="word", state="disabled"
        )
        self.txt_log.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))

        scrollbar = tk.Scrollbar(log_panel, command=self.txt_log.yview, bg=BG_CARD, bd=0, highlightthickness=0)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))
        self.txt_log.config(yscrollcommand=scrollbar.set)

        # Right Column (Thinking Board Panel Frame)
        self.thinking_pane = tk.Frame(self.right_pane, bg=BG_MAIN, width=320)
        self.thinking_pane.pack(side="right", fill="both", expand=False, padx=(10, 20), pady=(10, 20))
        self.thinking_pane.pack_propagate(False)

        tb_panel = tk.Frame(self.thinking_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        tb_panel.pack(fill="both", expand=True)

        tb_title = tk.Label(tb_panel, text="AI THOUGHT PROCESS / LUỒNG SUY NGHĨ", font=self.ui_font, fg=COLOR_MUTED, bg=BG_CARD)
        tb_title.pack(anchor="w", padx=15, pady=(10, 10))

        # Secondary 3x3 grid (read-only labels/buttons for visual process)
        tb_grid_container = tk.Frame(tb_panel, bg=BG_CARD, padx=5, pady=5)
        tb_grid_container.pack(pady=5)

        self.thinking_cells = []
        for i in range(9):
            row = i // 3
            col = i % 3
            cell = tk.Label(
                tb_grid_container, text="", font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
                bg=COLOR_GRID, fg=COLOR_TEXT, width=4, height=1, relief="flat", bd=0
            )
            cell.grid(row=row, column=col, padx=4, pady=4)
            self.thinking_cells.append(cell)

        # Simulation metrics
        self.lbl_sim_depth = tk.Label(tb_panel, text="Simulation Depth (Độ sâu): -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_sim_depth.pack(anchor="w", padx=15, pady=2)

        self.lbl_sim_score = tk.Label(tb_panel, text="Simulated Score (Điểm thử): -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_sim_score.pack(anchor="w", padx=15, pady=2)

        self.lbl_sim_alpha = tk.Label(tb_panel, text="Alpha: -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_sim_alpha.pack(anchor="w", padx=15, pady=2)

        self.lbl_sim_beta = tk.Label(tb_panel, text="Beta: -", font=self.subtitle_font, fg=COLOR_TEXT, bg=BG_CARD)
        self.lbl_sim_beta.pack(anchor="w", padx=15, pady=2)

        # Separator line
        sep = tk.Frame(tb_panel, height=1, bg=COLOR_GRID)
        sep.pack(fill="x", padx=15, pady=10)

        # Animation Speed Slider
        speed_label = tk.Label(tb_panel, text="Animation Speed / Tốc độ (ms):", font=self.subtitle_font, fg=COLOR_MUTED, bg=BG_CARD)
        speed_label.pack(anchor="w", padx=15)

        self.speed_slider = tk.Scale(
            tb_panel, from_=20, to=1000, orient="horizontal", variable=self.animation_speed,
            bg=BG_CARD, fg=COLOR_TEXT, highlightthickness=0, troughcolor=COLOR_GRID,
            activebackground=COLOR_BTN_HOVER, resolution=10, cursor="hand2"
        )
        self.speed_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Skip Animation Checkbutton
        self.chk_skip_anim = tk.Checkbutton(
            tb_panel, text="Skip Animation (Chạy ngay)", variable=self.skip_animation,
            font=self.subtitle_font, bg=BG_CARD, fg=COLOR_TEXT, selectcolor=BG_MAIN,
            activebackground=BG_CARD, activeforeground=COLOR_TEXT, cursor="hand2"
        )
        self.chk_skip_anim.pack(anchor="w", padx=15, pady=5)

    # --- UI Interactions ---

    def on_btn_hover(self, event, button):
        """Highlights the grid square on hover if it's empty and selectable."""
        if not self.game_over and not self.ai_thinking and button["text"] == "":
            button.config(bg=COLOR_HOVER)

    def on_btn_leave(self, event, button):
        """Reverts the grid square background when the mouse leaves."""
        if button["text"] == "":
            button.config(bg=COLOR_GRID)

    def write_log(self, text):
        """Helper to write message to the log widget."""
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, text + "\n")
        self.txt_log.config(state="disabled")
        self.txt_log.see(tk.END)

    def clear_logs(self):
        """Clears all text in the log widget."""
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.config(state="disabled")

    def change_role(self, role):
        """Changes the human player's role (X or O) and restarts the game."""
        if self.ai_thinking:
            return
        self.human_player = role
        self.ai_player = "O" if role == "X" else "X"
        self.reset_game()

    def change_algo(self, algo):
        """Changes the active AI search algorithm."""
        if self.ai_thinking:
            return
        self.selected_algo = algo
        self.update_algo_selector_ui()
        # Reset game on algo change to keep comparison clear
        self.reset_game()

    def update_role_selector_ui(self):
        """Highlights the currently selected role button."""
        if self.human_player == "X":
            self.btn_select_x.config(bg=COLOR_X, fg=BG_MAIN, activebackground=COLOR_X, activeforeground=BG_MAIN)
            self.btn_select_o.config(bg=COLOR_GRID, fg=COLOR_O, activebackground=COLOR_HOVER, activeforeground=COLOR_O)
        else:
            self.btn_select_x.config(bg=COLOR_GRID, fg=COLOR_X, activebackground=COLOR_HOVER, activeforeground=COLOR_X)
            self.btn_select_o.config(bg=COLOR_O, fg=BG_MAIN, activebackground=COLOR_O, activeforeground=BG_MAIN)

    def update_algo_selector_ui(self):
        """Highlights the currently selected algorithm button."""
        algos = {
            "minimax": self.btn_algo_minimax,
            "alpha_beta": self.btn_algo_alphabeta,
            "expectimax": self.btn_algo_expectimax
        }
        for name, btn in algos.items():
            if self.selected_algo == name:
                btn.config(bg=COLOR_BTN, fg=BG_MAIN, activebackground=COLOR_BTN, activeforeground=BG_MAIN)
            else:
                btn.config(bg=COLOR_GRID, fg=COLOR_TEXT, activebackground=COLOR_HOVER, activeforeground=COLOR_TEXT)

    # --- Game Logic ---

    def reset_game(self):
        """Resets the board state and starts a new game."""
        self.cancel_thinking_animation()
        self.board = [""] * 9
        self.game_over = False
        self.ai_thinking = False
        self.current_turn = "X"
        
        self.update_role_selector_ui()
        self.update_algo_selector_ui()
        self.reset_metrics_ui()
        self.clear_logs()
        self.write_log("System Ready. Make your move or wait for AI.")
        
        # Reset UI cells
        for btn in self.buttons:
            btn.config(text="", bg=COLOR_GRID, fg=COLOR_TEXT, state="normal")

        # Reset thinking board cells
        for cell in self.thinking_cells:
            cell.config(text="", bg=COLOR_GRID, fg=COLOR_TEXT)

        # Reset simulated metrics
        self.lbl_sim_depth.config(text="Simulation Depth (Độ sâu): -")
        self.lbl_sim_score.config(text="Simulated Score (Điểm thử): -")
        self.lbl_sim_alpha.config(text="Alpha: -")
        self.lbl_sim_beta.config(text="Beta: -")

        self.update_status()

        # If AI goes first
        if self.ai_player == "X":
            self.trigger_ai_move()

    def reset_metrics_ui(self):
        """Resets the search metrics displayed in the dashboard."""
        self.lbl_nodes.config(text="States Explored (Trạng thái duyệt): -")
        self.lbl_cuts.config(text="Pruning Cuts (Lần cắt tỉa): -")
        self.lbl_time.config(text="Calculation Time (Thời gian chạy): -")

    def update_status(self):
        """Updates the game status label message."""
        if self.game_over:
            return

        if self.current_turn == self.human_player:
            self.status_label.config(text=f"Your Turn ({self.human_player})", fg=COLOR_TEXT)
        else:
            self.status_label.config(text="AI is thinking...", fg=COLOR_MUTED)

    def on_cell_click(self, index):
        """Handles grid cell clicks by the user."""
        if self.game_over or self.ai_thinking or self.board[index] != "":
            return

        # Player move
        self.make_move(index, self.human_player)
        
        # Check game state
        if not self.check_game_end():
            # Pass turn to AI
            self.current_turn = self.ai_player
            self.update_status()
            self.trigger_ai_move()

    def make_move(self, index, player):
        """Executes a move on the logical board and updates the UI."""
        self.board[index] = player
        color = COLOR_X if player == "X" else COLOR_O
        self.buttons[index].config(text=player, fg=color, disabledforeground=color, state="disabled")

    def trigger_ai_move(self):
        """Schedules the AI move with a small delay for better user experience."""
        self.ai_thinking = True
        self.root.after(300, self.execute_ai_move)

    def execute_ai_move(self):
        """Finds and performs the AI's move using the selected algorithm."""
        if self.game_over:
            self.ai_thinking = False
            return
            
        start_time = time.perf_counter()
        
        if self.selected_algo == "minimax":
            best_index, nodes, logs, thinking_steps = minimax.find_best_move(self.board, self.ai_player)
            cuts_text = "N/A (Minimax)"
        elif self.selected_algo == "expectimax":
            best_index, nodes, logs, thinking_steps = expectimax.find_best_move(self.board, self.ai_player)
            cuts_text = "N/A (Expectimax)"
        else:
            best_index, nodes, cuts, logs, thinking_steps = alpha_beta.find_best_move(self.board, self.ai_player)
            cuts_text = f"{cuts:,}"

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # If skip animation is checked or we have no thinking steps, execute immediately
        if self.skip_animation.get() or not thinking_steps:
            # Update metrics UI
            self.lbl_nodes.config(text=f"States Explored (Trạng thái duyệt): {nodes:,}")
            self.lbl_cuts.config(text=f"Pruning Cuts (Lần cắt tỉa): {cuts_text}")
            self.lbl_time.config(text=f"Calculation Time (Thời gian chạy): {elapsed_ms:.2f} ms")

            # Update Logs UI
            self.clear_logs()
            if thinking_steps:
                for step in thinking_steps:
                    log_line = step.get('log', '')
                    if log_line:
                        self.write_log(log_line)
                self.write_log("-" * 40)
            for log_line in logs:
                self.write_log(log_line)

            # Perform the actual move
            if best_index is not None:
                self.make_move(best_index, self.ai_player)
            
            self.ai_thinking = False
            
            # Check game state
            if not self.check_game_end():
                # Pass turn to player
                self.current_turn = self.human_player
                self.update_status()
        else:
            # Start the playback animation
            self.start_thinking_animation(best_index, thinking_steps, nodes, cuts_text, elapsed_ms, logs)

    # --- Thinking Process Animation ---

    def start_thinking_animation(self, best_index, thinking_steps, final_nodes, final_cuts_text, final_elapsed_ms, final_logs):
        self.ai_thinking = True
        self.thinking_steps = thinking_steps
        self.current_step_index = 0
        self.clear_logs()
        self.write_log("AI Engine: Analyzing possibilities / Đang phân tích...")

        # Store parameters for when the animation completes
        self.final_best_index = best_index
        self.final_nodes = final_nodes
        self.final_cuts_text = final_cuts_text
        self.final_elapsed_ms = final_elapsed_ms
        self.final_logs = final_logs

        self.play_next_thinking_step()

    def play_next_thinking_step(self):
        if not self.ai_thinking:
            return

        if self.current_step_index >= len(self.thinking_steps):
            self.complete_thinking_animation()
            return

        step = self.thinking_steps[self.current_step_index]
        self.current_step_index += 1

        # 1. Update thinking board cells
        board_state = step.get('board', [""] * 9)
        active_move = step.get('move', None)
        
        for idx in range(9):
            val = board_state[idx]
            color = COLOR_X if val == "X" else COLOR_O
            self.thinking_cells[idx].config(text=val, fg=color)
            
            if idx == active_move:
                self.thinking_cells[idx].config(bg=COLOR_HOVER)
            else:
                self.thinking_cells[idx].config(bg=COLOR_GRID)

        # 2. Update metrics
        self.lbl_sim_depth.config(text=f"Simulation Depth (Độ sâu): {step.get('depth', '-')}")
        
        score_val = step.get('score', None)
        if score_val is not None:
            if isinstance(score_val, float):
                self.lbl_sim_score.config(text=f"Simulated Score (Điểm thử): {score_val:.2f}")
            else:
                self.lbl_sim_score.config(text=f"Simulated Score (Điểm thử): {score_val}")
        else:
            self.lbl_sim_score.config(text="Simulated Score (Điểm thử): Evaluating...")

        alpha_val = step.get('alpha', None)
        beta_val = step.get('beta', None)
        self.lbl_sim_alpha.config(text=f"Alpha: {alpha_val if alpha_val is not None else 'N/A'}")
        self.lbl_sim_beta.config(text=f"Beta: {beta_val if beta_val is not None else 'N/A'}")

        # 3. Add to logs
        log_line = step.get('log', '')
        if log_line:
            self.write_log(log_line)

        # Schedule next step
        speed = self.animation_speed.get()
        self.animation_after_id = self.root.after(speed, self.play_next_thinking_step)

    def complete_thinking_animation(self):
        # Reset thinking board cell highlights
        for idx in range(9):
            self.thinking_cells[idx].config(bg=COLOR_GRID)

        # Update metrics UI
        self.lbl_nodes.config(text=f"States Explored (Trạng thái duyệt): {self.final_nodes:,}")
        self.lbl_cuts.config(text=f"Pruning Cuts (Lần cắt tỉa): {self.final_cuts_text}")
        self.lbl_time.config(text=f"Calculation Time (Thời gian chạy): {self.final_elapsed_ms:.2f} ms")

        # Append final logs rather than clearing
        self.write_log("-" * 40)
        for log_line in self.final_logs:
            self.write_log(log_line)

        # Perform the actual move
        if self.final_best_index is not None:
            self.make_move(self.final_best_index, self.ai_player)

        self.ai_thinking = False
        self.animation_after_id = None

        # Check game state
        if not self.check_game_end():
            self.current_turn = self.human_player
            self.update_status()

    def cancel_thinking_animation(self):
        if self.animation_after_id:
            self.root.after_cancel(self.animation_after_id)
            self.animation_after_id = None
        self.ai_thinking = False

    def check_game_end(self):
        """Checks if the game has ended, highlights winning combo if any, and updates status."""
        winner, combo = alpha_beta.check_winner_and_combo(self.board)
        if winner:
            self.game_over = True
            # Highlight the winning combination dynamically
            if combo:
                for idx in combo:
                    self.buttons[idx].config(bg=COLOR_WIN, fg=COLOR_WIN_TEXT, disabledforeground=COLOR_WIN_TEXT)
            
            # Winner status
            if winner == self.human_player:
                self.status_label.config(text="Congratulations! You Won!", fg=COLOR_WIN)
            else:
                self.status_label.config(text="AI Wins! Better luck next time.", fg=COLOR_X)
            return True

        if alpha_beta.is_board_full(self.board):
            self.game_over = True
            self.status_label.config(text="It's a draw!", fg=COLOR_MUTED)
            # Subtle draw background change for entire board
            for btn in self.buttons:
                btn.config(bg=COLOR_HOVER)
            return True

        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
