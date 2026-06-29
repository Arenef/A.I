class Expectimax:
    def __init__(self, ai_player):
        self.ai_player = ai_player
        self.opponent = 'O' if ai_player == 'X' else 'X'
        self.nodes_evaluated = 0
        self.logs = ["Expectimax Engine: Starting move search..."]
        self.thinking_steps = []

    def check_winner(self, board):
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] != '':
                return board[i]
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != '':
                return board[i]
        if board[0] == board[4] == board[8] != '':
            return board[0]
        if board[2] == board[4] == board[6] != '':
            return board[2]
        return None

    def is_board_full(self, board):
        return '' not in board

    def get_available_moves(self, board):
        return [i for i, cell in enumerate(board) if cell == '']

    def expectimax_search(self, current_board, depth, is_maximizing, last_move=None):
        self.nodes_evaluated += 1

        winner = self.check_winner(current_board)
        is_terminal = winner is not None or self.is_board_full(current_board)

        if len(self.thinking_steps) < 120 and last_move is not None:
            mover = self.opponent if is_maximizing else self.ai_player
            role_desc = "AI" if mover == self.ai_player else "Opponent (Chance)"
            row = last_move // 3 + 1
            col = last_move % 3 + 1
            msg = f"Depth {depth}: {role_desc} simulates {mover} at Cell {last_move} (Row {row}, Col {col})"
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
                eval_score, _ = self.expectimax_search(current_board, depth + 1, False, move)
                current_board[move] = ''
                
                if depth == 0:
                    row = move // 3 + 1
                    col = move % 3 + 1
                    self.logs.append(f"└─ Evaluating Cell {move} (Row {row}, Col {col}): Expected Score = {eval_score:.2f}")

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

            if len(self.thinking_steps) < 120 and last_move is not None:
                row = last_move // 3 + 1
                col = last_move % 3 + 1
                self.thinking_steps.append({
                    'board': list(current_board),
                    'move': last_move,
                    'depth': depth,
                    'is_maximizing': is_maximizing,
                    'type': 'backtrack',
                    'log': f"Depth {depth}: Backtracking from Cell {last_move} (Row {row}, Col {col}) with Expected Score = {max_eval:.2f}",
                    'score': max_eval
                })
            return max_eval, best_move
        else:
            total_eval = 0
            for move in available_moves:
                current_board[move] = self.opponent
                eval_score, _ = self.expectimax_search(current_board, depth + 1, True, move)
                current_board[move] = ''
                total_eval += eval_score
            
            expected_value = total_eval / len(available_moves)

            if len(self.thinking_steps) < 120 and last_move is not None:
                row = last_move // 3 + 1
                col = last_move % 3 + 1
                self.thinking_steps.append({
                    'board': list(current_board),
                    'move': last_move,
                    'depth': depth,
                    'is_maximizing': is_maximizing,
                    'type': 'backtrack',
                    'log': f"Depth {depth}: Chance Node at Cell {last_move} (Row {row}, Col {col}) evaluates to Expected Value = {expected_value:.2f}",
                    'score': expected_value
                })
            return expected_value, None

    def find_best_move(self, board):
        max_val, best_move = self.expectimax_search(board, 0, True)
        if best_move is not None:
            row = best_move // 3 + 1
            col = best_move % 3 + 1
            self.logs.append(f"Expectimax Selection: Cell {best_move} (Row {row}, Col {col}) with Expected Score = {max_val:.2f}")
        else:
            self.logs.append("Expectimax Selection: No moves available.")
        
        self.logs.append(f"Expectimax Summary: Checked {self.nodes_evaluated} nodes.")
        return best_move, self.nodes_evaluated, self.logs, self.thinking_steps


def find_best_move(board, ai_player):
    engine = Expectimax(ai_player)
    return engine.find_best_move(board)


