import heapq

class UCS_Vaccum:
    def __init__(self):
        self.pq = []
        start_node = [[[0, 0, 1, 1],
                       [0, 2, -1, 1],
                       [1, -1, 1, 1],
                       [1, 0, 0, 1]], None, "START", 0]
        
        self.counter = 0 # biến thứ tự giúp tránh TypeError
        heapq.heappush(self.pq, (0, self.counter, start_node))
        self.reached = set()
        self.reached.add((0, self.matrix_to_tuple(start_node[0])))
        self.start = start_node[0]

    def matrix_to_tuple(self, matrix):
        return tuple(tuple(row) for row in matrix)
    
    def get_location(self, node):
        room = node[0]
        for i in range(len(room)):
            for j in range(len(room[0])):
                if room[i][j] == 2:
                    return i, j
        return None, None
    
    def possible_move(self, node):
        x, y = self.get_location(node)
        matrix = node[0]
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
    
    def solve(self):
        while len(self.pq) != 0:
            priority, counter, node = heapq.heappop(self.pq)

            if self.is_goal(node):
                return node
            
            move = self.possible_move(node)
            for m in move:
                new_node = self.act(node, m)
                state_tuple = (new_node[3], self.matrix_to_tuple(new_node[0]))
                if state_tuple not in self.reached:
                    self.counter += 1
                    heapq.heappush(self.pq, (new_node[3], self.counter, new_node))
                    self.reached.add(state_tuple)

        return None
            
    def act(self, node, action):
        x, y = self.get_location(node)
        matrix = [row[:] for row in node[0]]
        tmp = matrix[x][y]
        matrix[x][y] = 0

        if action == "up":
            matrix[x-1][y] = tmp
        
        if action == "down":
            matrix[x+1][y] = tmp
        
        if action == "left":
            matrix[x][y-1] = tmp

        if action == "right":
            matrix[x][y+1] = tmp

        new_node = (matrix, node, action, node[3] + 1)
        return new_node
            
    def is_goal(self, node):
        room = node[0]
        for i in range(len(room)):
            for j in range(len(room[0])):
                if room[i][j] == 1:
                    return False
                
        return True

    def get_path(self, node):
        path = []
        while node != None:
            path.append((node[0], node[2]))
            node = node[1]
        
        path.reverse()
        return path
    
    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j], end = " ")
            print()

    def run(self):
        node = self.solve()

        if node == None:
            print("Không có lời giải")
            return

        path = self.get_path(node)

        for i, p in enumerate(path):
            print(f"Step: {i+1}")
            self.print_matrix(p[0])
            print(f"Action: {p[1]}")
            print("=" * 15)
        
        print("!!!Căn phòng đã sạch sẽ hoàn toàn")

if __name__ == "__main__":
    vaccum = UCS_Vaccum()
    vaccum.run()
