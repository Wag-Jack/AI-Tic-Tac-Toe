#Imports
import copy
import math
import random

import constants as c
import tictactoe as ttt

from time import time

#Main function for Monte Carlo Tree Search
def mcts(board, performance):
    #Start timer to gather information on performance
    start_time = time()
    
    #Ensure the amount of states visited initialized to zero
    performance.states_visited = 0

    #Terminal condition does not need to be expanded or explored
    if ttt.terminal(board):
        #End timer and calculate execution time
        end_time = time()
        performance.add_elapse(end_time - start_time)
        performance.states_visited = 1
        #Since there's nothing to examine, return a null move
        return (-1,-1)
    
    #Create the tree and computational budget of MCTS
    root = c.Tree(board)
    budget = 1000

    #Iterate through the phases of MCTS until budget runs out
    while budget > 0:
        #Set our current node as the root
        node = root

        # SELECTION
        while not node.is_leaf() and node.is_fully_expanded() and not ttt.terminal(node.state): #and fully expanded
            node = selection(node)
            performance.states_visited += 1

        # EXPANSION
        if not ttt.terminal(node.state):
            node = expand(node)
            performance.states_visited += 1

        # SIMULATION 
        result = simulation(node, performance)

        # BACKPROPAGATION
        backpropagate(node, result)

        #Decrease budget upon completion of iteration
        budget -= 1

    if root.children: #Ensures that the Monte Carlo Tree was created 
        #After budget exhausted, choose the most confident child from resulting tree
        chosen_child = choose_best_child(root)

        #End timer and calculate execution time
        end_time = time()
        performance.add_elapse(end_time - start_time)

        #Return the randomly chosen child's resulting move
        return chosen_child.move
    else: #In the event the root is a terminal state
        #End timer and calculate execution time
        end_time = time()
        performance.add_elapse(end_time - start_time)
        
        #Return the root's resulting move
        return root.move

#Function to calculate the Upper Confidence Bound (UCB)
def ucb(board):
    """
    UCB = (w/n) + c*sqrt(log(t)/n)
    """
    #Constants
    w = board.wins #amount of simulated wins for current board state
    n = board.visits #amount of simulations occuring for current board state after ith move
    C = math.sqrt(2) #Exploration parameter

    #total amount of simulations that have occured after i moves
    if board.parent:
        t = board.parent.visits
    else:
        t = 1 #default for root
        
    #If node not visited, set to score of infinity
    if n == 0:
        return c.MAX
         
    #Exploitation term
    exploitation = w / n
    
    #Exploration term
    exploration = C * math.sqrt((math.log(t)) / n)

    #Returning final calculation
    return exploitation + exploration

#Function for selection phase of Monte Carlo Tree Search
def selection(node):
    #Avoid selecting leaf nodes
    while not node.is_leaf():
        #If the possible move is not already a child
        if node.additional_moves:
            #Child chosen to expand in next phase
            return node
        
        #Determine the UCB of each child of this node
        node = max(node.children, key=ucb)
    
    #Return a leaf node if selected
    return node

#Function for expansion phase of Monte Carlo Tree Search
def expand(node):
    #Cannot expand a node that has no more moves to make
    if not node.additional_moves:
        return node
    
    #Choose one potential move to make
    move = node.additional_moves.pop()
    
    #Apply the move to a copy of the node's game board state
    child_state = ttt.resultant(node.state, move)

    #Create a child node of this created state
    child_node = node.add_child(child_state, move)

    #Return the newly created child for simulation
    return child_node

#Function for simulation phase of Monte Carlo Tree Search
def simulation(node, performance):
    #Simulating a terminal mode simply means getting its result
    if ttt.terminal(node.state):
        result = ttt.result(node.state)
        return result
    
    #Create a deep copy of the current board
    current = copy.deepcopy(node.state)

    #Simulate the current game board until we reach a terminal state
    while not ttt.terminal(current):
        performance.states_visited += 1

        #Get a list of possible moves to make
        moves = list(ttt.actions(current))
        if not moves:
            break

        #Ensures that we don't simulate a terminal board more than we need to
        terminal_found = False

        # Prioritize terminal moves
        for move in moves:
            #Check what the next board state will be by applying a move
            next = ttt.resultant(current, move)
            
            #Check if this node was terminal
            if ttt.terminal(next):
                #If this node was terminal, go to it and stop iterating through moves
                current = next
                terminal_found = True
                break
        
        if not terminal_found: # no terminal state -> proceed with random move
            #Choose a random move to make
            random_move = random.choice(moves)

            #Apply random move to current board
            current = ttt.resultant(current, random_move)

    #Determine what the result of this simulation was
    result = ttt.result(current)
    
    #Return result for backpropagation
    return result

#Function for backpropagation phase of Monte Carlo Tree Search
def backpropagate(node, result):    
    #Backpropagate from current node back up to the root
    while node is not None:
        #Update amount of visits for each player
        node.visits += 1
        
        #Only update win if the right condition for player at root state
        if (result == 1 and node.player == c.X) or (result == -1 and node.player == c.O):
            node.wins += 1
        """
        elif result == 0:
            #Count draws as half a win in order to encourage optimal moves
            node.wins += 0.5
        """

        #Move back up the tree
        node = node.parent

        #Alternate result as we move up and deal with different players
        result = -result

#function to help choose the best child from the resulting Monte Carlo Tree
def choose_best_child(node):
    #Initialize variables
    highest_win_rate = c.MIN
    optimal_children = list()

    #Iterate through every single child of the tree
    for child in node.children:
        
        #Skip any unvisited children
        if child.visits == 0:
            continue 
        
        #Compute the exploration term
        child_win_rate = child.wins / child.visits

        #Check if the recently computed exploitation term is larger than the current largest
        if child_win_rate > highest_win_rate:
            highest_win_rate = child_win_rate
            optimal_children = [child] #should become the only optimal child choice
        #Equal exploitation term to highest means multiple options for an optimal choice
        elif child_win_rate == highest_win_rate:
            optimal_children.append(child)

    #Handle any errors with no optimal children found
    if not optimal_children:
        raise ValueError('No optimal children, error in search process')
    
    #Return a random choice of possible optimal children
    return random.choice(optimal_children)