import copy
import math
import random

import constants as c
import tictactoe as ttt

from constants import Tree
from time import time

def mcts(board, performance):
    start_time = time()
    
    if board == ttt.initial():
        end_time = time()
        performance.add_elapse(end_time - start_time)
        return random.choice(list(ttt.actions(board)))
    
    if ttt.terminal(board):
        end_time = time()
        performance.add_elapse(end_time - start_time)
        return (-1,-1)
    
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

    if root.children:
        chosen_child = choose_best_child(root)
        end_time = time()
        performance.add_elapse(end_time - start_time)
        return chosen_child.move
    else:
        end_time = time()
        performance.add_elapse(end_time - start_time)
        return root.move

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
    if ttt.terminal(node.state):
        result = ttt.result(node.state)
        return result
    
    current = copy.deepcopy(node.state)

    while not ttt.terminal(current):
        moves = list(ttt.actions(current))
        if not moves:
            break

        terminal_found = False
        # Prioritize terminal moves
        for move in moves:
            next = ttt.resultant(current, move)
            if ttt.terminal(next):
                current = next
                terminal_found = True
                break
        
        if not terminal_found: # no terminal state -> proceed with random move
            random_move = random.choice(moves)
            current = ttt.resultant(current, random_move)

    result = ttt.result(current)
    #print(f"Simulation result: {result} for final state {ttt.print_board(current)}")
    return result

def backpropagate(node, result):    
    #Backpropagate from current node back up to the root
    while node is not None:
        #Update amount of visits for each player
        node.visits += 1
        
        #Only update win if the right condition for player at root state
        if (result == 1 and node.player == c.X) or (result == -1 and node.player == c.O):
            node.wins += 1
        elif result == 0:
            node.wins += 0.5

        #print(f"Backpropagating node {node.move}: Wins = {node.wins}, Visits = {node.visits}, Result = {result}")

        #Move up the tree
        node = node.parent

        #Alternate result as we move up and deal with different players
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