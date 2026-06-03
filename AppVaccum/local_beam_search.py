import random

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path
    
    def __lt__(self, other):
        return self.cost_path < other.cost_path
    
class local_beam_search:
    def __init__(self, k=2):
        self.k = k
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
    
    def best_choice(self, frontier):
        min_val = 10e9
        best_choice_list = []

        for node in frontier:
            if node.cost_path < min_val:
                min_val = node.cost_path
        
        for node in frontier:
            if node.cost_path == min_val:
                best_choice_list.append(node)
        
        return best_choice_list

    def solve(self):
        current_state_set = [self.start_node]
        
        step_limit = 1000
        steps = 0
        
        while steps < step_limit:
            steps += 1
            neighbor_states = []
            
            for node in current_state_set:
                moves = self.possible_move(node)
                for m in moves:
                    new_node = self.act(node, m)
                    neighbor_states.append(new_node)
            
            if not neighbor_states:
                return None
                
            for node in neighbor_states:
                if self.is_goal(node):
                    return node

            neighbor_states.sort(key=lambda x: x.cost_path)
            
            current_state_set = neighbor_states[:self.k]
            
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
    vaccum = local_beam_search()
    vaccum.run()
