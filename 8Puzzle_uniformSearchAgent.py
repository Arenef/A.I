from collections import deque


class eight_puzzle:
    def __init__(self):
        self.q = deque()
        self.q.append(
            ([[0, 1, 3], 
              [4, 2, 6], 
              [7, 5, 8]], None, None, 0)
        )
        self.visited_matrix = [[[0, 1, 3], [4, 2, 6], [7, 5, 8]]]
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_location(self, node):
        matrix = node[0]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    return i, j
                
    def possible_move(self, node):
        x, y = self.get_location(node)
        move = []
        if x > 0: 
            move.append("up")
        if x < len(node[0]) - 1:
            move.append("down")
        if y > 0:
            move.append("left")
        if y < len(node[0][0]) - 1:
            move.append("right")
        return move
    
    def is_goal(self, node):
        matrix = node[0]
        for i in range(len(self.goal)):
            for j in range(len(self.goal[0])):
                if self.goal[i][j] != matrix[i][j]:
                    return False
        return True
    
    def bfs(self):
        
        while self.q:
            node = self.q.popleft()

            if self.is_goal(node):
                return node

            move = self.possible_move(node)
            
            for m in move:
                matrix = [row[:] for row in node[0]]
                x, y = self.get_location(node)
                tmp = matrix[x][y]
                if  m == "up":
                    matrix[x][y] = matrix[x-1][y]
                    matrix[x-1][y] = tmp
                
                if m == "down":
                    matrix[x][y] = matrix[x+1][y]
                    matrix[x+1][y] = tmp
                
                if m == "left":
                    matrix[x][y] = matrix[x][y-1]
                    matrix[x][y-1] = tmp

                if m == "right":
                    matrix[x][y] = matrix[x][y+1]
                    matrix[x][y+1] = tmp
                
                if (matrix, node, m, node[3] + 1) not in self.q and matrix not in self.visited_matrix:
                    self.q.append((matrix, node, m, node[3] + 1))
                    self.visited_matrix.append(matrix)
        return None
    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j], end = ' ')
            print()

    def path(self, node):
        path = []

        while node:
            path.append((node[0], node[2]))
            node = node[1]
        
        path.reverse()
        return path
    
    def run(self):
        
        
        node = self.bfs()
        path = self.path(node)

        finished_flag = True
        if node == None:
            finished_flag = False
        
        for i, p in enumerate(path):
            print(f"Step: {i+1}")
            self.print_matrix(p[0])
            if p[1] == None:
                print("-" * 15)
                continue
            print("Action:", p[1])
            print("-" * 15)
        
        if finished_flag:
            print("\n!!!A.I đã giải được trò chơi")
        else: 
            print("\n!!!A.I không thể giải được trò chơi trên")
        

game = eight_puzzle()
game.run()
