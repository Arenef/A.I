from collections import deque

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state          
        self.parent = parent        
        self.act = act              
        self.cost_path = cost_path  

class partially_observable:
    def __init__(self):
        self.frontier = deque()
        
        self.goals = (
            (
                (1, 2, 3),
                (4, 5, 6),
                (7, 8, 0)
            ),
            (
                (1, 2, 3),
                (8, 0, 4),
                (7, 6, 5)
            )
        )
       
        s1 = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 0, 8)
        )
        s2 = (
            (1, 2, 3),
            (8, 6, 4),
            (7, 0, 5)
        )
        s3 = (
            (1, 2, 3),
            (8, 4, 0),
            (7, 6, 5)
        )
        
        self.start = (s1, s2, s3)
        start_node = Node(self.start, None, "START", 0)
        self.frontier.append(start_node)
        self.reached = set()
        self.reached.add(self.matrix_to_tuple(self.start))

    def get_location(self, physical_state):
        for i in range(len(physical_state)):
            for j in range(len(physical_state[0])):
                if physical_state[i][j] == 0:
                    return i, j
        return None, None
                
    def possible_move(self, node):
        return ["up", "down", "left", "right"]
    
    def transition(self, state, move):
        if state in self.goals:
            return state
        
        x, y = self.get_location(state)
        nx, ny = x, y
        if move == "up":
            nx -= 1
        elif move == "down":
            nx += 1
        elif move == "left":
            ny -= 1
        elif move == "right":
            ny += 1

        if 0 <= nx < 3 and 0 <= ny < 3:
            matrix = [list(row) for row in state]
            matrix[x][y], matrix[nx][ny] = matrix[nx][ny], matrix[x][y]
            return tuple(tuple(row) for row in matrix)
        return state

    def act(self, node, move):
        next_states = []
        for state in node.state:
            next_states.append(self.transition(state, move))
        new_belief = tuple(next_states)
        return Node(new_belief, node, move, node.cost_path + 1)
    
    def is_goal(self, node):
        return all(state in self.goals for state in node.state)
    
    def solve(self):
        start_node = self.frontier[0]
        if self.is_goal(start_node):
            return start_node

        while self.frontier:
            node = self.frontier.popleft()
            move = self.possible_move(node)

            for m in move:
                new_node = self.act(node, m)

                if self.is_goal(new_node):
                    return new_node

                state_tuple = self.matrix_to_tuple(new_node.state)
                if state_tuple not in self.reached:
                    self.reached.add(state_tuple)
                    self.frontier.append(new_node)
        return None
    
    def matrix_to_tuple(self, belief_state):
        return belief_state
    
    def get_path(self, node):
        path = []
        while node != None:
            path.append((node.state, node.act))
            node = node.parent
        path.reverse()
        return path
    
    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j], end = " ")
            print() 

    def print_start_pattern(self):
        print("Trạng thái bắt đầu dự đoán (chỉ biết vị trí 1 và 2):")
        print("1 2 ?")
        print("? ? ?")
        print("? ? ?")
        print("=" * 25)

    def print_goals(self):
        print("Goal state:")
        for idx, goal in enumerate(self.goals):
            print(f"Trạng thái Goal #{idx + 1}:")
            self.print_matrix(goal)
        print("=" * 25)

    def run(self):
        print("Máy giải 8-puzzle bằng tìm kiếm Belief State bắt đầu hoạt động\n")
        self.print_start_pattern()
        self.print_goals()
        node = self.solve()

        if node == None:
            print("Không tìm thấy lời giải conformant")
            return 

        path = self.get_path(node)

        for i, p in enumerate(path):
            print(f'Step: {i}')
            print(f'Action: {p[1]}')
            belief_state = p[0]
            print(f'Kích thước Belief State: {len(belief_state)}')
            for idx, state in enumerate(belief_state):
                print(f'  Trạng thái khả thi #{idx + 1}:')
                self.print_matrix(state)
            print("=" * 25)

        actions = [p[1] for p in path if p[1] != "START"]
        print(f"Solution Path: {' -> '.join(actions)}")

if __name__ == "__main__":
    solver = partially_observable()
    solver.run()
