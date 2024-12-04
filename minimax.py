import constants as c
import tictactoe as ttt

def minimax(board):
    if ttt.terminal(board):
        return None
    
    curr = ttt.current_player(board)

    if curr == c.X: #X will be the max player (find max of min_value())
        score = c.MIN
        optimal_move = None
        alpha = c.MIN
        beta = c.MAX

        for a in ttt.actions(board):
            val = min_value(ttt.resultant(board, a), alpha, beta)

            if val > score:
                score = val
                optimal_move = a

            alpha = max(alpha, score)
            if alpha >= beta:
                break

    else: #O will be the min player (fid min of max_value())
        score = c.MAX
        optimal_move = None
        alpha = c.MIN
        beta = c.MAX

        for a in ttt.actions(board):
            val = max_value(ttt.resultant(board, a), alpha, beta)

            if val < score:
                score = val
                optimal_move = a

            beta = min(beta, score)
            if alpha >= beta:
                break

    return optimal_move


def max_value(board, alpha, beta):
    if ttt.terminal(board):
        return ttt.result(board)
    
    v = c.MIN

    for a in ttt.actions(board):
        v = max(v, min_value(ttt.resultant(board, a), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v


def min_value(board, alpha, beta):
    if ttt.terminal(board):
        return ttt.result(board)
    
    v = c.MAX

    for a in ttt.actions(board):
        v = min(v, max_value(ttt.resultant(board, a), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break

    return v