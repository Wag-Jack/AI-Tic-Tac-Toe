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
        while node.children and not ttt.terminal(node.state): #and fully expanded
            node = selection(node)

        # EXPANSION
        if not ttt.terminal(node.state):
            node = expand(node)

        # SIMULATION
        result = simulation(node)

        # BACKPROPAGATION
        update_statistics(node, result)

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
    highest_UCB = c.MIN
    selected_child = None

    for child in node.children:
        child_UCB = ucb(child)
        if child_UCB > highest_UCB:
            highest_UCB = child_UCB
            selected_child = child

    return selected_child

def expand(node):
    # Ensures there are moves to analyze
    if not node.additional_moves:
        node.additional_moves = list(ttt.actions(node.state))
    
    # Double check that we have moves to expand
    if node.additional_moves:
        move = node.additional_moves.pop()
        child_state = ttt.resultant(node.state, move) #result of applying move to node.state
        child_node = c.Tree(child_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node
    
    # Return the expanded node
    return node

def simulation(node):
    current = copy.deepcopy(node.state)

    while not ttt.terminal(current):
        moves = list(ttt.actions(current))
        if not moves:
            break

        random_move = random.choice(moves)
        current = ttt.resultant(current, random_move)

    return ttt.result(current)

def update_statistics(node, result):    
    while node is not None:
        node.visits += 1
        current_player = ttt.current_player(node.state)
        if result == 1 and current_player == c.X:
            node.wins += 1
        elif result == -1 and current_player == c.O:
            node.wins -= 1
        elif result == 1 and current_player == c.O:
            node.wins -= 1
        elif result == -1 and current_player == c.X:
            node.wins += 1

        node = node.parent

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