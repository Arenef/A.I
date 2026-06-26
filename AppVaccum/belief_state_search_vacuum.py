from collections import deque

class Node():
    def __init__(self, state, parent, act, cost_path):
        self.state = state          
        self.parent = parent        
        self.act = act              
        self.cost_path = cost_path  

class belief_state_search_vacuum:
    def __init__(self):
        self.frontier = deque()
        
        self.goal = (
            (0, 0, 0, 0),
            (0, 2, -1, 0),
            (0, -1, 0, 0),
            (0, 0, 0, 0)
        )
        
        s1 = (
            (2, 0, 1, 1),
            (0, 0, -1, 1),
            (1, -1, 1, 1),
            (1, 0, 0, 1)
        )
        
        s2 = (
            (0, 2, 1, 1),
            (0, 0, -1, 1),
            (1, -1, 1, 1),
            (1, 0, 0, 1)
        )
        
        s3 = (
            (0, 0, 1, 1),
            (2, 0, -1, 1),
            (1, -1, 1, 1),
            (1, 0, 0, 1)
        )
        
        s4 = (
            (0, 0, 1, 1),
            (0, 2, -1, 1),
            (1, -1, 1, 1),
            (1, 0, 0, 1)
        )
        
        self.start = (s1, s2, s3, s4)
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
        if state == self.goal:
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
        return all(state == self.goal for state in node.state)
    
    def solve(self):
        self.search_events = []
        start_node = self.frontier[0]
        self.search_events.append((start_node.state, f"Khởi đầu Belief State có {len(start_node.state)} trạng thái khả thi."))
        if self.is_goal(start_node):
            return start_node

        while self.frontier:
            node = self.frontier.pop()
            self.search_events.append((node.state, f"Lấy Belief State khỏi frontier. Kích thước: {len(node.state)}, Hành động trước: {node.act}"))
            move = self.possible_move(node)

            for m in move:
                new_node = self.act(node, m)

                if self.is_goal(new_node):
                    self.search_events.append((new_node.state, f"Tìm thấy đích! Belief State: {len(new_node.state)} trạng thái khả thi."))
                    return new_node

                state_tuple = self.matrix_to_tuple(new_node.state)
                if state_tuple not in self.reached:
                    self.reached.add(state_tuple)
                    self.frontier.append(new_node)
                    self.search_events.append((new_node.state, f"Thêm Belief State vào frontier. Hành động: {m}, Kích thước: {len(new_node.state)}"))
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
        print("Máy hút bụi giải bằng tìm kiếm Belief State bắt đầu hoạt động")
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
    solver = belief_state_search_vacuum()
    solver.run()
