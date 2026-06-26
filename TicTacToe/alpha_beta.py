class AlphaBeta:
    def __init__(self, ai_player):
        self.ai_player = ai_player
        self.opponent = 'O' if ai_player == 'X' else 'X'
        self.nodes_evaluated = 0
        self.pruning_cuts = 0
        self.logs = ["Alpha-Beta Engine: Starting move search..."]
        self.thinking_steps = []

    def check_winner_and_combo(self, board):
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] != '':
                return board[i], (i, i+1, i+2)
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != '':
                return board[i], (i, i+3, i+6)
        if board[0] == board[4] == board[8] != '':
            return board[0], (0, 4, 8)
        if board[2] == board[4] == board[6] != '':
            return board[2], (2, 4, 6)
        return None, None

    def check_winner(self, board):
        winner, _ = self.check_winner_and_combo(board)
        return winner

    def is_board_full(self, board):
        return '' not in board

    def get_available_moves(self, board):
        return [i for i, cell in enumerate(board) if cell == '']

    def minimax_search(self, current_board, depth, alpha, beta, is_maximizing, last_move=None):
        self.nodes_evaluated += 1

        winner = self.check_winner(current_board)
        is_terminal = winner is not None or self.is_board_full(current_board)

        if len(self.thinking_steps) < 120 and last_move is not None:
            mover = self.opponent if is_maximizing else self.ai_player
            role_desc = "AI" if mover == self.ai_player else "Opponent"
            row = last_move // 3 + 1
            col = last_move % 3 + 1
            msg = f"Depth {depth}: {role_desc} simulates {mover} at Cell {last_move} (Row {row}, Col {col}) [Alpha={alpha}, Beta={beta}]"
            if is_terminal:
                if winner:
                    msg += f" -> Terminal: {winner} wins!"
                else:
                    msg += " -> Terminal: Draw!"
            
            self.thinking_steps.append({
                'board': list(current_board),
                'move': last_move,
                'depth': depth,
                'is_maximizing': is_maximizing,
                'alpha': alpha,
                'beta': beta,
                'type': 'terminal' if is_terminal else 'visit',
                'log': msg,
                'score': None
            })

        if winner == self.ai_player:
            return 10 - depth, None
        if winner == self.opponent:
            return depth - 10, None
        if self.is_board_full(current_board):
            return 0, None

        available_moves = self.get_available_moves(current_board)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in available_moves:
                current_board[move] = self.ai_player
                eval_score, _ = self.minimax_search(current_board, depth + 1, alpha, beta, False, move)
                current_board[move] = ''
                
                if depth == 0:
                    row = move // 3 + 1
                    col = move % 3 + 1
                    self.logs.append(f"└─ Evaluating Cell {move} (Row {row}, Col {col}): Score = {eval_score} [Alpha={alpha}, Beta={beta}]")

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.pruning_cuts += 1
                    if depth <= 2 and len(self.logs) < 35:
                        self.logs.append(f"   ├── [Pruning Cut Maximizer] at depth {depth} (beta={beta} <= alpha={alpha})")
                    
                    if len(self.thinking_steps) < 120:
                        self.thinking_steps.append({
                            'board': list(current_board),
                            'move': move,
                            'depth': depth,
                            'is_maximizing': is_maximizing,
                            'alpha': alpha,
                            'beta': beta,
                            'type': 'prune',
                            'log': f"Depth {depth}: Pruning remaining moves because beta={beta} <= alpha={alpha}",
                            'score': None
                        })
                    break
            
            if len(self.thinking_steps) < 120 and last_move is not None:
                row = last_move // 3 + 1
                col = last_move % 3 + 1
                self.thinking_steps.append({
                    'board': list(current_board),
                    'move': last_move,
                    'depth': depth,
                    'is_maximizing': is_maximizing,
                    'alpha': alpha,
                    'beta': beta,
                    'type': 'backtrack',
                    'log': f"Depth {depth}: Backtracking from Cell {last_move} (Row {row}, Col {col}) with Score = {max_eval}",
                    'score': max_eval
                })
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in available_moves:
                current_board[move] = self.opponent
                eval_score, _ = self.minimax_search(current_board, depth + 1, alpha, beta, True, move)
                current_board[move] = ''
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.pruning_cuts += 1
                    if depth <= 2 and len(self.logs) < 35:
                        self.logs.append(f"   ├── [Pruning Cut Minimizer] at depth {depth} (beta={beta} <= alpha={alpha})")
                    
                    if len(self.thinking_steps) < 120:
                        self.thinking_steps.append({
                            'board': list(current_board),
                            'move': move,
                            'depth': depth,
                            'is_maximizing': is_maximizing,
                            'alpha': alpha,
                            'beta': beta,
                            'type': 'prune',
                            'log': f"Depth {depth}: Pruning remaining moves because beta={beta} <= alpha={alpha}",
                            'score': None
                        })
                    break

            if len(self.thinking_steps) < 120 and last_move is not None:
                row = last_move // 3 + 1
                col = last_move % 3 + 1
                self.thinking_steps.append({
                    'board': list(current_board),
                    'move': last_move,
                    'depth': depth,
                    'is_maximizing': is_maximizing,
                    'alpha': alpha,
                    'beta': beta,
                    'type': 'backtrack',
                    'log': f"Depth {depth}: Backtracking from Cell {last_move} (Row {row}, Col {col}) with Score = {min_eval}",
                    'score': min_eval
                })
            return min_eval, best_move

    def find_best_move(self, board):
        max_val, best_move = self.minimax_search(board, 0, float('-inf'), float('inf'), True)
        if best_move is not None:
            row = best_move // 3 + 1
            col = best_move % 3 + 1
            self.logs.append(f"Alpha-Beta Selection: Cell {best_move} (Row {row}, Col {col}) with Score = {max_val}")
        else:
            self.logs.append("Alpha-Beta Selection: No moves available.")
        
        self.logs.append(f"Alpha-Beta Summary: Checked {self.nodes_evaluated} nodes, performed {self.pruning_cuts} cuts.")
        return best_move, self.nodes_evaluated, self.pruning_cuts, self.logs, self.thinking_steps


def check_winner_and_combo(board):
    helper = AlphaBeta('X')
    return helper.check_winner_and_combo(board)


def check_winner(board):
    helper = AlphaBeta('X')
    return helper.check_winner(board)


def is_board_full(board):
    helper = AlphaBeta('X')
    return helper.is_board_full(board)


def get_available_moves(board):
    helper = AlphaBeta('X')
    return helper.get_available_moves(board)


def find_best_move(board, ai_player):
    engine = AlphaBeta(ai_player)
    return engine.find_best_move(board)

