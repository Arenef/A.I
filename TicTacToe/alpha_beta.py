def check_winner_and_combo(board):
    """
    Checks the board for a winner dynamically.
    Returns:
        (str, tuple): (winner ('X' or 'O' or None), winning_combo (tuple of indices or None))
    """
    # Rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != '':
            return board[i], (i, i+1, i+2)
    # Columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != '':
            return board[i], (i, i+3, i+6)
    # Diagonals
    if board[0] == board[4] == board[8] != '':
        return board[0], (0, 4, 8)
    if board[2] == board[4] == board[6] != '':
        return board[2], (2, 4, 6)
    return None, None

def check_winner(board):
    """
    Checks the board for a winner.
    Args:
        board (list): A list of 9 elements.
    Returns:
        str: 'X' or 'O' if there is a winner, None otherwise.
    """
    winner, _ = check_winner_and_combo(board)
    return winner

def is_board_full(board):
    return '' not in board

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == '']

def find_best_move(board, ai_player):
    opponent = 'O' if ai_player == 'X' else 'X'
    nodes_evaluated = 0
    pruning_cuts = 0
    logs = ["Alpha-Beta Engine: Starting move search..."]

    def minimax_search(current_board, depth, alpha, beta, is_maximizing):
        nonlocal nodes_evaluated, pruning_cuts
        nodes_evaluated += 1

        winner = check_winner(current_board)
        if winner == ai_player:
            return 10 - depth, None
        if winner == opponent:
            return depth - 10, None
        if is_board_full(current_board):
            return 0, None

        available_moves = get_available_moves(current_board)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in available_moves:
                current_board[move] = ai_player
                eval_score, _ = minimax_search(current_board, depth + 1, alpha, beta, False)
                current_board[move] = ''  # Backtrack
                
                if depth == 0:
                    row = move // 3 + 1
                    col = move % 3 + 1
                    logs.append(f"└─ Evaluating Cell {move} (Row {row}, Col {col}): Score = {eval_score} [Alpha={alpha}, Beta={beta}]")

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    pruning_cuts += 1
                    if depth <= 2 and len(logs) < 35:
                        logs.append(f"   ├── [Pruning Cut Maximizer] at depth {depth} (beta={beta} <= alpha={alpha})")
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in available_moves:
                current_board[move] = opponent
                eval_score, _ = minimax_search(current_board, depth + 1, alpha, beta, True)
                current_board[move] = ''  # Backtrack
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    pruning_cuts += 1
                    if depth <= 2 and len(logs) < 35:
                        logs.append(f"   ├── [Pruning Cut Minimizer] at depth {depth} (beta={beta} <= alpha={alpha})")
                    break
            return min_eval, best_move

    max_val, best_move = minimax_search(board, 0, float('-inf'), float('inf'), True)
    if best_move is not None:
        row = best_move // 3 + 1
        col = best_move % 3 + 1
        logs.append(f"Alpha-Beta Selection: Cell {best_move} (Row {row}, Col {col}) with Score = {max_val}")
    else:
        logs.append("Alpha-Beta Selection: No moves available.")
    
    logs.append(f"Alpha-Beta Summary: Checked {nodes_evaluated} nodes, performed {pruning_cuts} cuts.")
    return best_move, nodes_evaluated, pruning_cuts, logs
