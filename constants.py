import tictactoe as ttt

E = ' '
O = 'O'     #Minimax value of -1
X = 'X'     #Minimax value of 1
T = 'tie'   #Minimax value of 0 (board.result() = none)

#MIN and MAX initial values for Minimax
MIN = float('-inf')
MAX = float('inf')

def in_bounds(x, y):
    return x in range(3) and y in range(3)

#Tree data structure for MCST
class Tree:
    def __init__(self, state, parent=None):
        self.state = state #Current board state
        self.parent = parent 
        self.children = []
        self.visits = 0 #Amount of times this board node has been visited
        self.wins = 0 #Amount of wins after visiting this node
        self.additional_moves = [] #populate based on current state's valid moves

    def add_child(self, child_state):
        child = Tree(child_state, self)
        self.children.append(child)
        return child
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def is_fully_expanded(self):
        return len(self.additional_moves) == 0
    
    def is_root(self):
        return self.parent is None