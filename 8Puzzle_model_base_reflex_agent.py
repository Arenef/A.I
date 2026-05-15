import random

class eight_puzzle:
    def __init__(self):
        self.matrix = [
            [1,2,3],
            [4,0,6],
            [7,5,8]
        ]
        self.location = []
        self.visited_matrices = []

        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]        
    def get_location(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 0:
                    self.location = [i, j]
        return None
    def possible_move(self):
        x, y = self.location[0], self.location[1]
        move = []
        opt_move = []
        # if x > 0 and self.matrix[x-1][y] not in self.visited_matrices:
        #     move.append("up")
        # if x < len(self.matrix) - 1 and self.matrix[x+1][y] not in self.visited_matrices:
        #     move.append("down")
        # if y > 0 and self.matrix[x][y-1] not in self.visited_matrices:
        #     move.append("left")
        # if y < len(self.matrix[0]) - 1 and self.matrix[x][y+1] not in self.visited_matrices:
        #     move.append("right")

        if x > 0: 
            move.append("up")

            matrix_copy = [row[:] for row in self.matrix]

            tmp = matrix_copy[x][y]
            matrix_copy[x][y] = matrix_copy[x-1][y]
            matrix_copy[x-1][y] = tmp

            if matrix_copy not in self.visited_matrices:
                opt_move.append("up")


        if x < len(self.matrix) - 1:
            move.append("down")

            matrix_copy = [row[:] for row in self.matrix]

            tmp = matrix_copy[x][y]
            matrix_copy[x][y] = matrix_copy[x+1][y]
            matrix_copy[x+1][y] = tmp

            if matrix_copy not in self.visited_matrices:
                opt_move.append("down")


        if y > 0:
            move.append("left")

            matrix_copy = [row[:] for row in self.matrix]

            tmp = matrix_copy[x][y]
            matrix_copy[x][y] = matrix_copy[x][y-1]
            matrix_copy[x][y-1] = tmp

            if matrix_copy not in self.visited_matrices:
                opt_move.append("left")


        if y < len(self.matrix[0]) - 1:
            move.append("right")

            matrix_copy = [row[:] for row in self.matrix]

            tmp = matrix_copy[x][y]
            matrix_copy[x][y] = matrix_copy[x][y+1]
            matrix_copy[x][y+1] = tmp

            if matrix_copy not in self.visited_matrices:
                opt_move.append("right")
                     
        if len(opt_move) != 0:
            return opt_move
        
        return move
    def rule(self):
        move = self.possible_move()
        return random.choice(move)


    def act(self, action):
        x, y = self.location[0], self.location[1]
        self.visited_matrices.append(self.matrix.copy())
        if action == "up":
            tmp = self.matrix[x][y]
            self.matrix[x][y] = self.matrix[x-1][y]
            self.matrix[x-1][y] = tmp
            self.location[0] -= 1
            
        if action == "down":
            tmp = self.matrix[x][y]
            self.matrix[x][y] = self.matrix[x+1][y]
            self.matrix[x+1][y] = tmp
            self.location[0] += 1
        
        if action == "left":
            tmp = self.matrix[x][y]
            self.matrix[x][y] = self.matrix[x][y-1]
            self.matrix[x][y-1] = tmp
            self.location[1] -= 1

        if action == "right":
            tmp = self.matrix[x][y]
            self.matrix[x][y] = self.matrix[x][y+1]
            self.matrix[x][y+1] = tmp
            self.location[1] += 1

    def print_matrix(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                print(self.matrix[i][j], end = " ")
            print()
    
    def is_goal(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] != self.goal[i][j]:
                    return False
        return True

    def run(self):
        self.get_location()
        for i in range(1000):
            print(f"Step: {i+1}")

            action = self.rule()
            print("Action:", action)

            self.act(action)
            if self.is_goal():
                self.print_matrix()
                print("\n!!!Hoàn thành trò chơi ")
                break
            
            self.print_matrix()
            print("-" * 15)
        
        if self.is_goal() is False:
            print("\n!!!A.I không thể hoàn thành trò chơi x_x")

game = eight_puzzle()
game.run()