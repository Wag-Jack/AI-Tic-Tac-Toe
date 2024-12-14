#imports
import constants as c
import tictactoe as ttt

from time import time

#Main minimax function with alpha-beta pruning
def minimax(board, performance):
    #Start timer to gather information on performance
    start_time = time()

    #Ensure the amount of states visited initialized as zero
    performance.states_visited = 0
    
    #Don't run minimax on a terminal state
    if ttt.terminal(board):
        #End timer and calculate execution time
        end_time = time()
        performance.add_elapse(end_time - start_time)
        performance.states_visited = 1
        #Return a null move
        return (-1,-1)
    
    #Get the current player to determine min / max player
    curr = ttt.current_player(board)

    if curr == c.X: #X will be the max player (find max of min_value())
        #Initialize variables
        score = c.MIN
        optimal_move = None
        alpha = c.MIN
        beta = c.MAX

        #Iterate through each possible action for this board state
        for a in ttt.actions(board):
            #Compute the minimum value
            val = min_value(ttt.resultant(board, a), alpha, beta, performance)

            #Determine the highest minimum value
            if val > score:
                score = val
                optimal_move = a

            #Set alpha as best possible minimum score
            alpha = max(alpha, score)
            #Prune the tree if alpha better than beta
            if alpha >= beta:
                break

    else: #O will be the min player (find min of max_value())
        #Initialize variables
        score = c.MAX
        optimal_move = None
        alpha = c.MIN
        beta = c.MAX

        #Iterate through each possible action for this board state
        for a in ttt.actions(board):
            #Compute the maximum value
            val = max_value(ttt.resultant(board, a), alpha, beta, performance)

            #Determine the lowest maximum value
            if val < score:
                score = val
                optimal_move = a

            #Set beta as best possible maximum score
            beta = min(beta, score)
            #Prune the tree if alpha better than beta
            if alpha >= beta:
                break

    #End timer and calculate execution time
    end_time = time()
    performance.add_elapse(end_time - start_time)
    #Return the optimal move determined by minimax
    return optimal_move

#Maximum value function for minimax
def max_value(board, alpha, beta, performance):
    #Increment the amount of states visited while traversing the algorithm
    performance.states_visited += 1
    
    #Return the result if we're currently at a terminal state
    if ttt.terminal(board):
        return ttt.result(board)
    
    #Set minimum v
    v = c.MIN

    #Iterate through all possible actions for the state
    for a in ttt.actions(board):
        #Switch between max_value and min_value, return the highest value
        v = max(v, min_value(ttt.resultant(board, a), alpha, beta, performance))
        #Determine alpha value
        alpha = max(alpha, v)
        #Prune the tree if alpha is better than beta
        if alpha >= beta:
            break

    #Return final maximum value
    return v

#Minimum value function for minimax
def min_value(board, alpha, beta, performance):
    #Increment the amount of states visited while traversing the algorithm
    performance.states_visited += 1
    
    #Return the result if we're currently at a terminal state
    if ttt.terminal(board):
        return ttt.result(board)
    
    #Set maximum v
    v = c.MAX

    #Iterate through all possible actions for the state
    for a in ttt.actions(board):
        #Switch between min_value and max_value, returning the lowest value
        v = min(v, max_value(ttt.resultant(board, a), alpha, beta, performance))
        #Determine beta value
        beta = min(beta, v)
        #Prune the tree if alpha is better than beta
        if alpha >= beta:
            break

    #Return final mimimum value
    return v