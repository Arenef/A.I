import heapq

class Node():
    def __init__(self, id, state, parent, act, cost_path, g):
        self.id = id
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path
        self.g = g
        # g(n): số nước đi từ lúc bắt đầu tới thời điểm hiện tại
        # h(n): số ô sai

    def __lt__(self, other):
        if self.cost_path == other.cost_path:
            return self.id < other.id

        return self.cost_path < other.cost_path
    
class ida_star_vacuum:
    def __init__(self):
        state =[
                [0, 0, 1, 1],
                [0, 2, -1, 0],
                [1, -1, 0, 0],
                [0, 0, 0, 1]]
        self.start = state
        self.counter = 0

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

        self.counter += 1
        return Node(self.counter, matrix, node, move, node.g + 1 + self.heuristic(matrix), node.g + 1)
    
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
        I = self.heuristic(self.start)
        
        while True:
            self.search_events.append((self.start, f"\n--- IDA* Lượt Tìm Kiếm (Ngưỡng I = {I}) ---"))
            node, alpha = self.search(I)
            
            if node != None:
                return node
            
            self.search_events.append((self.start, f"Không tìm thấy giải pháp dưới ngưỡng I = {I}. Tăng ngưỡng I thêm {alpha}"))
            I += alpha

            if I == float("inf"):
                return None

    def search(self, I):
        frontier = []
        start_node = Node(self.counter, self.start, None, "START", self.heuristic(self.start), 0)
        heapq.heappush(frontier, start_node)
        self.search_events.append((start_node.state, f"  Thêm node khởi đầu vào frontier: Vị trí {self.get_location(start_node)}, f(n): {start_node.cost_path} (g: {start_node.g}, h: {start_node.cost_path - start_node.g})"))
        
        self.reached = set()
        self.reached.add(self.matrix_to_tuple(self.start))
        alpha = 10e9
        while frontier:
            node = heapq.heappop(frontier)
            self.search_events.append((node.state, f"  Lấy node khỏi frontier: Vị trí {self.get_location(node)}, Hành động: {node.act}, f(n): {node.cost_path} (g: {node.g}, h: {node.cost_path - node.g})"))

            if node.cost_path < alpha:
               alpha = node.cost_path

            if self.is_goal(node):
                self.search_events.append((node.state, f"  -> Đạt trạng thái đích ở vị trí: {self.get_location(node)}"))
                return node, alpha
            
            move = self.possible_move(node)

            for m in move:
                new_node = self.act(node, m)

                if new_node.cost_path >= I:
                    self.search_events.append((new_node.state, f"  -> Từ chối láng giềng: Vị trí {self.get_location(new_node)} (f(n): {new_node.cost_path} >= giới hạn I: {I})"))
                elif self.matrix_to_tuple(new_node.state) in self.reached:
                    pass
                else:
                    self.reached.add(self.matrix_to_tuple(new_node.state))
                    heapq.heappush(frontier, new_node)
                    self.search_events.append((new_node.state, f"  -> Thêm node vào frontier: Vị trí {self.get_location(new_node)}, Hành động: {new_node.act}, f(n): {new_node.cost_path} (g: {new_node.g}, h: {new_node.cost_path - new_node.g})"))

        return None, alpha
    
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
    vaccum = ida_star_vacuum()
    vaccum.run()
