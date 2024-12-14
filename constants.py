#Imports
import tictactoe as ttt

#Constant values for board states
E = ' '
O = 'O'     #Minimax value of -1
X = 'X'     #Minimax value of 1

#MIN and MAX set as -inf and +inf respectively
MIN = float('-inf')
MAX = float('inf')

#Helper function to ensure input is within range of board
def in_bounds(x, y):
    return x in range(3) and y in range(3)

#Tree data structure for MCST
class Tree:
    #Constructor for tree nodes
    def __init__(self, state, parent=None, move=None):
        self.state = state #Current board state
        self.parent = parent #Parent node this state is connected to
        self.move = move #Move which resulted in the node's board state
        self.children = [] #List of all children to the node
        self.visits = 0 #Amount of times this board node has been visited
        self.wins = 0 #Amount of wins after visiting this node
       
        #Determines who the next player is for this state
        self.player = ttt.current_player(self.state)

        #Determine how many more and what moves could be made at the given state
        if ttt.terminal(self.state):
            self.additional_moves = [] #No moves left for a terminal state
        else:
            self.additional_moves = ttt.actions(self.state) #Pull all possible moves for state

    #Helper function to add a child to the tree
    def add_child(self, child_state, move):
        child = Tree(child_state, self, move) #Create tree node with child state and move to get to child
        self.children.append(child) #Add child node to the tree itself
        return child
   
    #Helper function to determine if current node is a leaf
    def is_leaf(self):
        return len(self.children) == 0 #Leaf nodes have no children
   
    #Helper function to determine if current node has reached full expansion
    def is_fully_expanded(self):
        return len(self.additional_moves) == 0 #Expanded nodes have no moves left
                                               #Either terminal or someone won
   
    #Helper function to determine what the root node is
    def is_root(self):
        return self.parent is None #Root node has no parents to it
    
class Performance:
    def __init__(self):
        self.prev_elapsed_time = 0
        self.all_prev_time = []
        self.states_visited = 0

    def add_elapse(self, time):
        self.prev_elapsed_time = time
        self.all_prev_time.append(time)