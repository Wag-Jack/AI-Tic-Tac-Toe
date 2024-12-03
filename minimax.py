import constants as c
from tictactoe import Board

def minimax(board):
    if board.terminal():
        return None
    
    curr = board.current_player()

    if curr == c.X: #X will be the max player (find max of min_value())
        score = float('-inf')
        optimal_move = None

        for a in board.actions():
            val = min_value(board.resultant(a))

            if val > score:
                score = val
                optimal_move = a

    else:
        score = float('inf')
        optimal_move = None

        for a in board.actions():
            val = max_value(board.resultant(a))

            if val < score:
                score = val
                optimal_move = a

    return optimal_move


def min_value(board):
    if board.terminal():
        return board.result()
    
    v = float('inf')

    for a in board.actions():
        v = min(v, max_value(board.resultant(a)))

    return v


def max_value(board):
    if board.terminal():
        return board.result()
    
    v = float('-inf')

    for a in board.actions():
        v = max(v, min_value(board.resultant(a)))

    return v