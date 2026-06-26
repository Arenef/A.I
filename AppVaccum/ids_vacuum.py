class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path

class ids_vacuum:
    def __init__(self):
        state =[
                [1, 0, 1, 0],
                [1, 2, -1, 0],
                [1, -1, 0, 0],
                [0, 0, 0, 0]]
        self.start = state
        self.reached_depth = {}

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

        return Node(matrix, node, move, node.cost_path + 1)
    
    def is_goal(self, node):
        matrix = node.state

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    return False
        return True
    
    def solve(self):
        self.search_events = []
        depth_limit = 0
        
        while True:
            self.search_events.append((self.start, f"\n--- IDS Lượt Tìm Kiếm (Giới hạn Độ sâu = {depth_limit}) ---"))
            
            result = self.dls(depth_limit)
            if result == "cutoff":
                depth_limit += 1
            elif result is None:
                # If search finished completely without cutoff, no solution exists
                return None
            else:
                return result

    def dls(self, limit):
        start_node = Node(self.start, None, "START", 0)
        self.reached_depth = {self.matrix_to_tuple(self.start): 0}
        return self.dls_recursive(start_node, limit)

    def dls_recursive(self, node, limit):
        self.search_events.append((node.state, f"Duyệt node: Vị trí {self.get_location(node)}, Độ sâu: {node.cost_path}, Hành động: {node.act}"))
        
        if self.is_goal(node):
            self.search_events.append((node.state, f"-> Tìm thấy trạng thái đích ở vị trí: {self.get_location(node)}"))
            return node
            
        if node.cost_path >= limit:
            self.search_events.append((node.state, f"-> Đạt giới hạn độ sâu ({limit}). Quay lui."))
            return "cutoff"
            
        any_cutoff = False
        moves = self.possible_move(node)
        for m in moves:
            child = self.act(node, m)
            child_state_tuple = self.matrix_to_tuple(child.state)
            
            if child_state_tuple in self.reached_depth and self.reached_depth[child_state_tuple] <= child.cost_path:
                continue
                
            self.reached_depth[child_state_tuple] = child.cost_path
            res = self.dls_recursive(child, limit)
            
            if res == "cutoff":
                any_cutoff = True
            elif res is not None:
                return res
                
        if any_cutoff:
            return "cutoff"
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
            print("Máy hút bụi gặp lỗi hoặc không tìm thấy lời giải")
            return 

        path = self.get_path(node)

        for i, p in enumerate(path):
            print(f'Step: {i+1}')
            self.print_matrix(p[0])
            print(f'Action: {p[1]}')
            print("=" * 15)

if __name__ == "__main__":
    vaccum = ids_vacuum()
    vaccum.run()
