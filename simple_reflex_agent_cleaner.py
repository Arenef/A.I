import random

def possible_move(x, y, n, m):
    move = []
    if x > 0: move.append('up')
    if x < m - 1: move.append('down')
    if y > 0: move.append('left')
    if y < n - 1: move.append('right')
    return move

def rules(lst, state):
    act = ""
    i, j = state[0], state[1]
    move = possible_move(i, j, len(lst[0]), len(lst))
    if lst[i][j] == 1:
        print('Hút bụi')
        lst[i][j] = 0
    act = random.choice(move)

    return act

def action(state, act):

    if act == 'up':
        state[0] -= 1
    if act == 'down':
        state[0] += 1
    if act == 'left':
        state[1] -= 1
    if act == 'right':
        state[1] += 1
    
    return state

def is_clean(room):

    for row in room:

        if 1 in row:
            return False

    return True

def main():

    # Ma trận phòng
    room = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 0, 0]
    ]

    # Vị trí robot ban đầu
    state = [1, 1]

    for step in range(100):

        print(f"\nStep {step + 1}")
        print("Vị trí của robot: ", state)
        # In phòng
        for i in range(len(room)):

            for j in range(len(room[0])):

                if [i, j] == state:
                    print("R", end=" ") # R là vị trí của robot
                else:
                    print(room[i][j], end=" ")

            print()

        # Rule match
        act = rules(room, state)

        print("Action:", act)

        # Action
        state = action(state, act)

        # Kiểm tra phòng đã sạch chưa
        if is_clean(room):
            print("\nRoom is clean!")
            break

main()
