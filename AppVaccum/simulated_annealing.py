import random
import math

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path
    
    def __lt__(self, other):
        return self.cost_path < other.cost_path
    
class simulated_annealing:
    def __init__(self, T0=10.0, Tmin=0.0001, alpha=0.99):
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha
        state = [
                [0, 0, 1, 1],
                [0, 2, -1, 1],
                [1, -1, 1, 1],
                [1, 0, 0, 1]
            ]
        self.start = state
        self.start_node = Node(state, None, "START", self.heuristic(state))

    def get_location(self, node):
        matrix = node.state
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 2:
                    return i, j
        return None, None
                
    def possible_move(self, node):
        matrix = node.state
        x, y = self.get_location(node)
        move = []

        if x > 0 and matrix[x-1][y] != -1:
            move.append("up")
        if x < len(matrix) - 1 and matrix[x+1][y] != -1:
            move.append("down")
        if y > 0 and matrix[x][y-1] != -1:
            move.append("left")
        if y < len(matrix[0]) - 1 and matrix[x][y+1] != -1:
            move.append("right")
        
        return move
    
    def act(self, node, move):
        matrix = [row[:] for row in node.state]
        x, y = self.get_location(node)
        tmp = matrix[x][y]
        matrix[x][y] = 0
        if move == "up":
            matrix[x-1][y] = tmp
        if move == "down":
            matrix[x+1][y] = tmp
        if move == "left":
            matrix[x][y-1] = tmp
        if move == "right":
            matrix[x][y+1] = tmp

        return Node(matrix, node, move, self.heuristic(matrix))
    
    def heuristic(self, matrix):
        score = 0 
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    score += 1
        return score
    
    def is_goal(self, node):
        matrix = node.state

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    return False
        return True
    
    def solve(self):
        self.search_events = []
        current_node = self.start_node
        T = self.T0
        self.search_events.append((current_node.state, f"Bắt đầu Simulated Annealing từ vị trí: {self.get_location(current_node)}, Heuristic: {current_node.cost_path}, T0: {T}"))
        
        while T > self.Tmin:
            if self.is_goal(current_node):
                self.search_events.append((current_node.state, f"  -> Tìm thấy đích: Vị trí {self.get_location(current_node)}"))
                return current_node
            
            moves = self.possible_move(current_node)
            if not moves:
                self.search_events.append((current_node.state, "Không tìm thấy di chuyển hợp lệ. Dừng tìm kiếm."))
                break
                
            m = random.choice(moves)
            next_node = self.act(current_node, m)
            self.search_events.append((next_node.state, f"Đánh giá láng giềng ngẫu nhiên: Vị trí {self.get_location(next_node)} qua hành động {m}, Heuristic: {next_node.cost_path}"))
            
            delta = next_node.cost_path - current_node.cost_path
            
            if delta < 0:
                self.search_events.append((next_node.state, f"  -> Chấp nhận láng giềng tốt hơn (Delta: {delta} < 0): Vị trí {self.get_location(next_node)}"))
                current_node = next_node
            else:
                p = math.exp(-delta / T)
                r = random.random()
                if r < p:
                    self.search_events.append((next_node.state, f"  -> Chấp nhận láng giềng tệ hơn với xác suất p = {p:.4f} > r = {r:.4f} (Nhiệt độ T: {T:.4f}): Vị trí {self.get_location(next_node)}"))
                    current_node = next_node
                else:
                    self.search_events.append((current_node.state, f"  -> Từ chối láng giềng tệ hơn (p = {p:.4f} <= r = {r:.4f})"))
            
            T = self.alpha * T
            
        if self.is_goal(current_node):
            self.search_events.append((current_node.state, f"  -> Tìm thấy đích ở trạng thái cuối: Vị trí {self.get_location(current_node)}"))
            return current_node
        return None
                
    def matrix_to_tuple(self, matrix):
        lst_1D = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                lst_1D.append(matrix[i][j])
        return tuple(lst_1D)
    
    def get_path(self, node):
        path = []

        while node != None:
            matrix = [row[:] for row in node.state]
            path.append((matrix, node.act))
            node = node.parent
        
        path.reverse()
        return path
    
    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j], end = " ")
            print() 

    def run(self):
        
        print("Máy hút bụi bắt đầu hoạt động")

        node = self.solve()

        if node == None:
            print("Máy hút bụi gặp lỗi")
            return 

        path = self.get_path(node)

        for i, p in enumerate(path):
            print(f'Step: {i+1}')
            self.print_matrix(p[0])
            print(f'Action: {p[1]}')
            print("=" * 15)
        
if __name__ == "__main__":
    vaccum = simulated_annealing()
    vaccum.run()
