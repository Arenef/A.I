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
        self.root.geometry("850x700")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        # Game State Variables
        self.human_player = "X"      # Human default
        self.ai_player = "O"         # AI default
        self.current_turn = "X"      # 'X' always starts
        self.board = [""] * 9
        self.game_over = False
        self.buttons = []
        self.ai_thinking = False     # Guard to prevent clicks during AI's turn
        
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
        # Split root into left (game) and right (logs) panes
        self.left_pane = tk.Frame(self.root, bg=BG_MAIN)
        self.left_pane.pack(side="left", fill="both", expand=True)

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

        # Thinking Log Panel
        log_panel = tk.Frame(self.right_pane, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground=COLOR_GRID)
        log_panel.pack(fill="both", expand=True, padx=(10, 30), pady=(10, 20))

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
        self.human_player = role
        self.ai_player = "O" if role == "X" else "X"
        self.reset_game()

    def change_algo(self, algo):
        """Changes the active AI search algorithm."""
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
            best_index, nodes, logs = minimax.find_best_move(self.board, self.ai_player)
            cuts_text = "N/A (Minimax)"
        elif self.selected_algo == "expectimax":
            best_index, nodes, logs = expectimax.find_best_move(self.board, self.ai_player)
            cuts_text = "N/A (Expectimax)"
        else:
            best_index, nodes, cuts, logs = alpha_beta.find_best_move(self.board, self.ai_player)
            cuts_text = f"{cuts:,}"

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Update metrics UI
        self.lbl_nodes.config(text=f"States Explored (Trạng thái duyệt): {nodes:,}")
        self.lbl_cuts.config(text=f"Pruning Cuts (Lần cắt tỉa): {cuts_text}")
        self.lbl_time.config(text=f"Calculation Time (Thời gian chạy): {elapsed_ms:.2f} ms")

        # Update Logs UI
        self.clear_logs()
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
