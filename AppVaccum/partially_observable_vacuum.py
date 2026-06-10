from collections import deque

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state          
        self.parent = parent        
        self.act = act              
        self.cost_path = cost_path  

class partially_observable_vacuum:
    def __init__(self):
        self.frontier = deque()
        
        g1 = (
            (0, 0, 0, 1),
            (1, 2, -1, 0),
            (0, -1, 0, 0),
            (1, 0, 0, 0)
        )
        g2 = (
            (0, 0, 0, 0),
            (0, 2, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        self.goals = (g1, g2)
        
        s1_clean = (
            (2, 0, 1, 1),
            (0, 0, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        s1_dirty = (
            (2, 0, 1, 1),
            (0, 0, -1, 0),
            (0, -1, 0, 0),
            (1, 0, 0, 0)
        )
        
        s2_clean = (
            (0, 2, 1, 1),
            (0, 0, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        s2_dirty = (
            (0, 2, 1, 1),
            (0, 0, -1, 0),
            (0, -1, 0, 0),
            (1, 0, 0, 0)
        )
        
        s3_clean = (
            (0, 0, 1, 1),
            (2, 0, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        s3_dirty = (
            (0, 0, 1, 1),
            (2, 0, -1, 0),
            (0, -1, 0, 0),
            (1, 0, 0, 0)
        )
        
        s4_clean = (
            (0, 0, 1, 1),
            (0, 2, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        s4_dirty = (
            (0, 0, 1, 1),
            (0, 2, -1, 0),
            (0, -1, 0, 0),
            (1, 0, 0, 0)
        )
        
        self.start = (s1_clean, s1_dirty, s2_clean, s2_dirty, s3_clean, s3_dirty, s4_clean, s4_dirty)
        start_node = Node(self.start, None, "START", 0)
        self.frontier.append(start_node)
        self.reached = set()
        self.reached.add(self.matrix_to_tuple(self.start))

    def get_location(self, physical_state):
        for i in range(len(physical_state)):
            for j in range(len(physical_state[0])):
                if physical_state[i][j] == 2:
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

        if 0 <= nx < len(state) and 0 <= ny < len(state[0]) and state[nx][ny] != -1:
            matrix = [list(row) for row in state]
            tmp = matrix[x][y]
            matrix[x][y] = 0   
            matrix[nx][ny] = tmp 
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

    def run(self):
        print("Máy hút bụi với quan sát một phần bắt đầu hoạt động\n")
        print("Trạng thái bắt đầu dự đoán (ô (3,0) có thể là 0 hoặc 1, vị trí robot chưa rõ):")
        print("? ? 1 1")
        print("? ? -1 ?")
        print("? -1 ? ?")
        print("? ? ? ?")
        print("=" * 25)
        
        print("Các trạng thái đích khả thi (chấp nhận ô (3,0) sạch hoặc bẩn):")
        for idx, goal in enumerate(self.goals):
            print(f"Goal khả thi #{idx + 1}:")
            self.print_matrix(goal)
        print("=" * 25)
        
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
    solver = partially_observable_vacuum()
    solver.run()
