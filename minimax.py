import constants as c
import tictactoe as ttt

def minimax(board):
    if ttt.terminal(board):
        return None
    
    curr = ttt.current_player(board)

    if curr == c.X: #X will be the max player (find max of min_value())
        score = float('-inf')
        optimal_move = None

        for a in ttt.actions(board):
            val = min_value(ttt.resultant(board, a))

            if val > score:
                score = val
                optimal_move = a

    else: #O will be the min player (fid min of max_value())
        score = float('inf')
        optimal_move = None

        for a in ttt.actions(board):
            val = max_value(ttt.resultant(board, a))

            if val < score:
                score = val
                optimal_move = a

    return optimal_move


def min_value(board):
    if ttt.terminal(board):
        return ttt.result(board)
    
    v = float('inf')

    for a in ttt.actions(board):
        v = min(v, max_value(ttt.resultant(board, a)))

    return v


def max_value(board):
    if ttt.terminal(board):
        return ttt.result(board)
    
    v = float('-inf')

    for a in ttt.actions(board):
        v = max(v, min_value(ttt.resultant(board, a)))

    return v