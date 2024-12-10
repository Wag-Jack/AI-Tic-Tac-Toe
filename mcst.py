import copy
import math
import random

import constants as c
import tictactoe as ttt

from constants import Tree

def mcst(board):
    root = c.Tree(board)
    budget = 100
    while budget > 0:
        node = root
        
        # SELECTION
        while node.children and not ttt.terminal(node.state): #and fully expanded
            node = selection(node)

        # EXPANSION
        if node.state != ttt.terminal(node.state):
            expand(node)

        # SIMULATION
        result = simulation(node)

        # BACKPROPAGATION
        while node != None:
            update_statistics(node, result)
            node = node.parent

        budget -= 1

    return choose_best_child(root)

def ucb(board):
    """
    UCB = (w/n) + c*sqrt(log(t)/n)
    """
    #Constants
    w = board.wins #amount of simulated wins for current board state
    n = board.visits #amount of simulations occuring for current board state after ith move
    c = math.sqrt(2) #Exploration parameter (TODO: make sure to check if this is fine)
    t = board.parent.visits #total amount of simulations that have occured after i moves

    #Exploitation term
    exploitation = w / n
    
    #Exploration term
    exploration = c * math.sqrt((math.log(t)) / n)

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
    if not node.additional_moves:
        actions = ttt.actions(node.state)
        for a in actions:
            node.additional_moves.append(a)
    else:
        for move in node.additional_moves:
            child_state = ttt.resultant(node.state, move) #result of applying move to node.state
            child_node = c.Tree(child_state)
            node.children.append(child_node)

def simulation(node):
    current = copy.deepcopy(node.state)
    moves = node.additional_moves

    while moves:
        index = random.randint(0, len(moves)-1)
        random_move = moves.pop(index)
        modified_state = ttt.resultant(current, random_move)
        current = modified_state

    return ttt.result(current)

def update_statistics(node, result):    
    node.visits += 1
    node.wins = result

def choose_best_child(node):
    highest_win_rate = c.MIN
    optimal_children = list()

    for child in node.children:
        child_win_rate = child.wins / child.visits
        if child_win_rate > highest_win_rate:
            highest_win_rate = child_win_rate
            optimal_children = [child]
        elif child_win_rate == highest_win_rate:
            optimal_children.append(child)

    return random.choice(optimal_children)