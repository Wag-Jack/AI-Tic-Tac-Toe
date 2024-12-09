from mcts import mcts
import tictactoe as ttt
import constants as c

board = [[c.X,c.E,c.E],
         [c.X,c.O,c.E],
         [c.O,c.X,c.O]]

while not ttt.terminal(board):
    optimal_move = mcts(board)
    board = ttt.resultant(board, optimal_move)
    ttt.print_board(board)