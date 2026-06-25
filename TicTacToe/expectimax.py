"""
Expectimax AI for Tic-Tac-Toe.
Chance nodes (opponent's turn) calculate the average of evaluation values for all legal moves (uniform distribution).
"""

def check_winner(board):
    """
    Checks the board for a winner.
    Args:
        board (list): A list of 9 elements ('X', 'O', or '').
    Returns:
        str: 'X' or 'O' if there is a winner, None otherwise.
    """
    # Rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != '':
            return board[i]
    # Columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != '':
            return board[i]
    # Diagonals
    if board[0] == board[4] == board[8] != '':
        return board[0]
    if board[2] == board[4] == board[6] != '':
        return board[2]
    return None

def is_board_full(board):
    """
    Checks if the board is full.
    Args:
        board (list): A list of 9 elements.
    Returns:
        bool: True if full, False otherwise.
    """
    return '' not in board

def get_available_moves(board):
    """
    Gets all empty indices on the board.
    Args:
        board (list): A list of 9 elements.
    Returns:
        list: Empty indices (0 to 8).
    """
    return [i for i, cell in enumerate(board) if cell == '']

def find_best_move(board, ai_player):
    """
    Finds the optimal move for the AI player using Expectimax.
    Args:
        board (list): A list of 9 elements ('X', 'O', or '').
        ai_player (str): 'X' or 'O'.
    Returns:
        tuple: (best_move, nodes_evaluated, logs)
    """
    opponent = 'O' if ai_player == 'X' else 'X'
    nodes_evaluated = 0
    logs = ["Expectimax Engine: Starting move search..."]

    def expectimax_search(current_board, depth, is_maximizing):
        nonlocal nodes_evaluated
        nodes_evaluated += 1

        # Base check for terminal states
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
                eval_score, _ = expectimax_search(current_board, depth + 1, False)
                current_board[move] = ''  # Backtrack
                
                # Log root level decisions
                if depth == 0:
                    row = move // 3 + 1
                    col = move % 3 + 1
                    logs.append(f"└─ Evaluating Cell {move} (Row {row}, Col {col}): Expected Score = {eval_score:.2f}")

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            # Chance node: average of all children
            total_eval = 0
            for move in available_moves:
                current_board[move] = opponent
                eval_score, _ = expectimax_search(current_board, depth + 1, True)
                current_board[move] = ''  # Backtrack
                total_eval += eval_score
            
            expected_value = total_eval / len(available_moves)
            return expected_value, None

    max_val, best_move = expectimax_search(board, 0, True)
    if best_move is not None:
        row = best_move // 3 + 1
        col = best_move % 3 + 1
        logs.append(f"Expectimax Selection: Cell {best_move} (Row {row}, Col {col}) with Expected Score = {max_val:.2f}")
    else:
        logs.append("Expectimax Selection: No moves available.")
    
    logs.append(f"Expectimax Summary: Checked {nodes_evaluated} nodes.")
    return best_move, nodes_evaluated, logs
