import random

class and_or_search_vacuum:
    def __init__(self):
        self.start = (
            (0, 0, 1, 1),
            (0, 2, -1, 1),
            (1, -1, 1, 1),
            (1, 0, 0, 1)
        )
        self.memo = {}

    def get_location(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 2:
                    return i, j
        return None, None

    def possible_move(self, state):
        x, y = self.get_location(state)
        move = []
        if x is None:
            return move

        if x > 0 and state[x-1][y] != -1:
            move.append("up")
        if x < len(state) - 1 and state[x+1][y] != -1:
            move.append("down")
        if y > 0 and state[x][y-1] != -1:
            move.append("left")
        if y < len(state[0]) - 1 and state[x][y+1] != -1:
            move.append("right")
        
        return move

    def results(self, state, action):
        x, y = self.get_location(state)
        if x is None:
            return [state]

        results_set = set()

        nx, ny = x, y
        if action == "up": nx -= 1
        elif action == "down": nx += 1
        elif action == "left": ny -= 1
        elif action == "right": ny += 1

        if 0 <= nx < len(state) and 0 <= ny < len(state[0]) and state[nx][ny] != -1:
            matrix = [list(row) for row in state]
            tmp = matrix[x][y]
            matrix[x][y] = 0
            matrix[nx][ny] = tmp
            results_set.add(tuple(tuple(row) for row in matrix))
        else:
            results_set.add(state)

        if action in ["up", "down"]:
            slip_moves = ["left", "right"]
        else:
            slip_moves = ["up", "down"]

        for move in slip_moves:
            sx, sy = x, y
            if move == "up": sx -= 1
            elif move == "down": sx += 1
            elif move == "left": sy -= 1
            elif move == "right": sy += 1

            if 0 <= sx < len(state) and 0 <= sy < len(state[0]) and state[sx][sy] != -1:
                matrix = [list(row) for row in state]
                tmp = matrix[x][y]
                matrix[x][y] = 0
                matrix[sx][sy] = tmp
                results_set.add(tuple(tuple(row) for row in matrix))
            else:
                results_set.add(state)

        return list(results_set)

    def is_goal_state(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 1:
                    return False
        return True

    def solve(self):
        self.memo = {}
        plan = self.or_search(self.start, [])
        return plan

    def or_search(self, state, path):
        if self.is_goal_state(state):
            return []
        if state in path:
            return "cycle"
        if state in self.memo:
            return self.memo[state]

        for action in self.possible_move(state):
            result_states = self.results(state, action)
            plan = self.and_search(result_states, path + [state])
            if plan is not None:
                self.memo[state] = [action, plan]
                return [action, plan]

        self.memo[state] = None
        return None

    def and_search(self, states, path):
        plans = {}
        for s in states:
            plan_s = self.or_search(s, path)
            if plan_s is None:
                return None
            plans[s] = plan_s
        return plans

    def get_path(self, plan):
        if plan is None:
            return [(self.start, "START")]
            
        path = []
        current_state = self.start
        path.append((current_state, "START"))
        
        curr_plan = plan
        step_limit = 100
        steps = 0
        while not self.is_goal_state(current_state) and steps < step_limit:
            if not curr_plan or curr_plan == "cycle":
                curr_plan = self.memo.get(current_state)
                if not curr_plan:
                    break
            
            action, outcomes_plans = curr_plan
            possible_results = self.results(current_state, action)
            
            next_state = random.choice(possible_results)
            path.append((next_state, action))
            
            curr_plan = outcomes_plans.get(next_state)
            current_state = next_state
            steps += 1
            
        return path

    def print_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                print(matrix[i][j], end = " ")
            print() 

    def run(self):
        print("AND-OR-GRAPH-SEARCH solver started")
        plan = self.solve()
        if plan is None:
            print("No plan found!")
            return

        print("Plan found successfully!")
        path = self.get_path(plan)
        for i, p in enumerate(path):
            print(f'Step: {i}')
            print(f'Action: {p[1]}')
            self.print_matrix(p[0])
            print("=" * 25)

if __name__ == "__main__":
    solver = and_or_search_vacuum()
    solver.run()
