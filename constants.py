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
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_state):
        child = Tree(child_state, self)
        self.children.append(child)
        return child
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def is_root(self):
        return self.parent is None