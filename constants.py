E = ' '
O = 'O'     #Minimax value of -1
X = 'X'     #Minimax value of 1
T = 'tie'   #Minimax value of 0 (board.result() = none)

MIN = float('-inf')
MAX = float('inf')

def in_bounds(x, y):
    return x in range(3) and y in range(3)