import random
import time

def possible_move(x, y, n, m):
    """Xác định các hướng có thể di chuyển của ô trống (0)"""
    move = []
    if x > 0: move.append('up')
    if x < m - 1: move.append('down')
    if y > 0: move.append('left')
    if y < n - 1: move.append('right')
    return move

def rules(state, n, m):
    """Đưa ra quyết định hành động ngẫu nhiên nhưng hợp lệ"""
    i, j = state[0], state[1]
    move = possible_move(i, j, n, m)
    act = random.choice(move)
    return act

def action(board, state, act):
    """Thực thi hành động: Hoán đổi ô trống (0) với ô liền kề theo hướng di chuyển"""
    i, j = state[0], state[1]
    new_i, new_j = i, j
    
    if act == 'up':
        new_i -= 1
    if act == 'down':
        new_i += 1
    if act == 'left':
        new_j -= 1
    if act == 'right':
        new_j += 1
        
    # Hoán đổi giá trị trên bàn cờ
    board[i][j], board[new_i][new_j] = board[new_i][new_j], board[i][j]
    
    # Cập nhật vị trí mới của ô trống (0)
    state[0], state[1] = new_i, new_j
    
    return state

def is_goal(board):
    """Kiểm tra xem bàn cờ đã đạt trạng thái đích chưa"""
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    return board == goal_state

def main():
    # Bàn cờ 8-puzzle ban đầu (số 0 là ô trống)
    board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]

    # Vị trí ban đầu của ô trống (0) đang ở hàng 2, cột 1 (index bắt đầu từ 0)
    state = [2, 1]
    
    n = len(board[0]) # Số cột
    m = len(board)    # Số hàng

    print("=== BẮT ĐẦU MÔ PHỎNG 8-PUZZLE ===")
    time.sleep(1)

    for step in range(100):
        print(f"\n[BƯỚC {step + 1}]")
        print("Vị trí của ô trống (0):", state)
        
        # In bàn cờ
        for i in range(m):
            for j in range(n):
                if board[i][j] == 0:
                    print("_", end=" ")
                else:
                    print(board[i][j], end=" ")
            print()

        # Kiểm tra điều kiện thắng
        if is_goal(board):
            print("\nTHÀNH CÔNG! Trò chơi đã được giải.")
            break

        # Rule-match
        act = rules(state, n, m)
        print("Action:", act)

        # Action
        state = action(board, state, act)
        
        time.sleep(0.3)
        
    else:
        print("\nTHẤT BẠI: Đã chạy 100 bước nhưng vẫn đi ngẫu nhiên chưa tới đích!")

if __name__ == "__main__":
    main()