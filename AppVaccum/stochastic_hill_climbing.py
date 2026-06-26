import random

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path
    
class stochastic_ascent_hill_climbing:
    def __init__(self):
        state = [
                [1, 2, 1, 0],
                [1, 0, 1, 0],
                [1, 1, 1, 0],
                [0, 0, 0, 0]
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
        self.search_events.append((current_node.state, f"Khởi đầu Stochastic Ascent từ vị trí: {self.get_location(current_node)}, Heuristic: {current_node.cost_path}"))
        
        while True:
            frontier = []
            move = self.possible_move(current_node)
            self.search_events.append((current_node.state, f"Lấy node hiện tại xét các láng giềng: Vị trí {self.get_location(current_node)}"))

            for m in move:
                new_node = self.act(current_node, m)
                self.search_events.append((new_node.state, f"  Đang đánh giá láng giềng: Vị trí {self.get_location(new_node)} qua hành động {m}, Heuristic: {new_node.cost_path}"))

                if self.is_goal(new_node):
                    self.search_events.append((new_node.state, f"  -> Đạt trạng thái đích ở vị trí: {self.get_location(new_node)}"))
                    return new_node
                
                if new_node.cost_path < current_node.cost_path:
                    frontier.append(new_node)
                    self.search_events.append((new_node.state, f"  -> Thêm vào frontier láng giềng tốt hơn: Vị trí {self.get_location(new_node)}, Heuristic: {new_node.cost_path}"))

            if len(frontier) == 0:
                self.search_events.append((current_node.state, "Frontier trống (Không tìm thấy láng giềng nào tốt hơn). Dừng tìm kiếm."))
                return None   

            current_node = random.choice(frontier) 
            self.search_events.append((current_node.state, f"Lấy ngẫu nhiên node từ frontier láng giềng: Vị trí {self.get_location(current_node)}, Heuristic: {current_node.cost_path}"))
    
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
    vaccum = stochastic_ascent_hill_climbing()
    vaccum.run()
