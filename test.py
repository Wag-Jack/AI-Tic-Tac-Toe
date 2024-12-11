from mcst import mcst
import tictactoe as ttt
import constants as c

board = [[c.E,c.E,c.E],
         [c.E,c.X,c.E],
         [c.E,c.E,c.E]]
optimal_move = mcst(board)

board = ttt.resultant(board, optimal_move)
ttt.print_board(board)