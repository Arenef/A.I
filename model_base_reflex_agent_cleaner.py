import random

class Vaccum:
    def __init__(self):
        # 0: Clean, 1: Dirty, -1: Vật cản
        self.room = [
            [1, 1, -1, 1],
            [1, -1, 1, 1], 
            [1, 1, 1, 1]
        ]
        self.visited = []

        self.index = [0, 0]
    
    def possible_move(self):
        x, y = self.index[0], self.index[1]
        move = []

        if x < len(self.room) - 1  and self.room[x+1][y] != -1: move.append('down')
        if x > 0 and self.room[x-1][y] != -1: move.append('up') 
        if y > 0 and self.room[x][y-1] != -1: move.append('left')
        if y < len(self.room[0]) - 1 and self.room[x][y+1] != -1: move.append('right')

        opt_move = move.copy()
        if "down" in move:
            if (x+1, y) in self.visited:
                opt_move.remove("down")
        if "up" in move:
            if (x-1, y) in self.visited:
                opt_move.remove("up")
        if "left" in move:
            if (x, y-1) in self.visited:
                opt_move.remove("left")
        if "right" in move:
            if (x, y+1) in self.visited:
                opt_move.remove("right")
        if len(opt_move) == 0:
            return move
        return opt_move
    
    def rule(self):
        if self.room[self.index[0]][self.index[1]] == 1:
            return "Suck"
        else:
            move = self.possible_move()
            return random.choice(move)
        
    def act(self, action):

        if (self.index[0], self.index[1]) not in self.visited:
            self.visited.append((self.index[0], self.index[1]))

        if action == "Suck":
            self.room[self.index[0]][self.index[1]] = 0
        
        if action == "up":
            self.index[0] -= 1
        if action == "down":
            self.index[0] += 1
        if action == "left":
            self.index[1] -= 1
        if action == "right":
            self.index[1] += 1
        
    
    def print_room(self):
        for i in range(len(self.room)):
            for j in range(len(self.room[0])):
                if i == self.index[0] and j == self.index[1]:
                    print("A", end = " ")
                else:
                    print(self.room[i][j], end = " ")
            print()

    def is_all_clean(self):
        for i in range(len(self.room)):
            for j in range(len(self.room[0])):
                if self.room[i][j] == 1:
                    return False
        return True
        
    def run(self):
        for i in range(100):
            print(f"Step: {i+1}")
            print("Room State: ")
            self.print_room()
            action = self.rule()

            self.act(action)
            
            if action != "Suck":
                action = "Move " + action
            print("Action:", action)

            if self.is_all_clean():
                print("\n!!!Phòng đã sạch sẽ hoàn toàn")
                break
            print('-' * 15)

        if self.is_all_clean() is False:
            print("\n!!!Phòng vẫn chưa sạch sẽ")

vaccum = Vaccum()
vaccum.run()
