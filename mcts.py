import copy
import math
import random

import constants as c
import tictactoe as ttt

from constants import Tree

def mcts(board):
    root = c.Tree(board)
    budget = 1000
    while budget > 0:
        node = root

        # SELECTION
        while not node.is_leaf() and node.is_fully_expanded() and not ttt.terminal(node.state): #and fully expanded
            node = selection(node)

        # EXPANSION
        if not ttt.terminal(node.state):
            node = expand(node)

        # SIMULATION
        result = simulation(node)

        # BACKPROPAGATION
        backpropagate(node, result)

        budget -= 1

    with open('tree_output.txt','w') as file:
        root.print_tree(file)
    chosen_child = choose_best_child(root)
    return chosen_child.move

def ucb(board):
    """
    UCB = (w/n) + c*sqrt(log(t)/n)
    """
    #Constants
    w = board.wins #amount of simulated wins for current board state
    n = board.visits #amount of simulations occuring for current board state after ith move
    C = math.sqrt(2) #Exploration parameter (TODO: make sure to check if this is fine)

    #total amount of simulations that have occured after i moves
    if board.parent:
        t = board.parent.visits
    else:
        t = 1 #default for root
        
    if n == 0:
        return c.MAX
         
    #Exploitation term
    exploitation = w / n
    
    #Exploration term
    exploration = C * math.sqrt((math.log(t)) / n)

    #Returning final calculation
    return exploitation + exploration

def selection(node):
    while not node.is_leaf():
        if node.additional_moves:
            return node
        node = max(node.children, key=ucb)
    return node

def expand(node):
    if not node.additional_moves:
        return node
    
    move = node.additional_moves.pop()
    child_state = ttt.resultant(node.state, move)
    child_node = node.add_child(child_state, move)
    return child_node

def simulation(node):
    current = copy.deepcopy(node.state)

    while not ttt.terminal(current):
        moves = list(ttt.actions(current))
        if not moves:
            break

        random_move = random.choice(moves)
        current = ttt.resultant(current, random_move)

    return ttt.result(current)

def backpropagate(node, result):    
    while node is not None:
        node.visits += 1
        #current_player = ttt.current_player(node.state)
        if result == 1 and node.player == c.X:
            node.wins += 1 #X win
        elif result == -1 and node.player == c.O:
            node.wins += 1 #O win

        node = node.parent

        # Flip the result to represent different players
        result = -result

def choose_best_child(node):
    highest_win_rate = c.MIN
    optimal_children = list()

    for child in node.children:
        if child.visits == 0:
            continue #skip unvisited children
        
        child_win_rate = child.wins / child.visits

        if child_win_rate > highest_win_rate:
            highest_win_rate = child_win_rate
            optimal_children = [child]
        elif child_win_rate == highest_win_rate:
            optimal_children.append(child)

    if not optimal_children:
        raise ValueError('No optimal children, error in search process')
    
    return random.choice(optimal_children)