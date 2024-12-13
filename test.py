from mcts import mcts
from minimax import minimax
import tictactoe as ttt
import constants as c

"""
1. Blank state
2. X in upper left corner
3. X in upper right corner
4. X in bottom right corner
5. X in bottom left corner
6. X in middle
7. XEE
   XOE
   OXO
8. XXE
   OOE
   EEE
9. XOO
   XEE
   EEE
10.XOX
   OXO
   OXE
11. XXE
    OEE
    EOE
12. XOX
    OXO
    EEX
13. XOX
    OXE
    EEO
14. XOE
    EXE
    OEE
"""

boards = [[[c.E,c.E,c.E],[c.E,c.E,c.E],[c.E,c.E,c.E]],
          [[c.X,c.E,c.E],[c.E,c.E,c.E],[c.E,c.E,c.E]],
          [[c.E,c.E,c.X],[c.E,c.E,c.E],[c.E,c.E,c.E]],
          [[c.E,c.E,c.E],[c.E,c.E,c.E],[c.E,c.E,c.X]],
          [[c.E,c.E,c.E],[c.E,c.E,c.E],[c.X,c.E,c.E]],
          [[c.E,c.E,c.E],[c.E,c.X,c.E],[c.E,c.E,c.E]],
          [[c.X,c.E,c.E],[c.X,c.O,c.E],[c.O,c.X,c.O]],
          [[c.X,c.X,c.E],[c.O,c.O,c.E],[c.E,c.E,c.E]],
          [[c.X,c.O,c.O],[c.X,c.E,c.E],[c.E,c.E,c.E]],
          [[c.X,c.O,c.X],[c.O,c.X,c.O],[c.O,c.X,c.E]],
          [[c.X,c.X,c.E],[c.O,c.E,c.E],[c.E,c.O,c.E]],
          [[c.X,c.O,c.X],[c.O,c.X,c.O],[c.E,c.E,c.X]],
          [[c.X,c.O,c.X],[c.O,c.X,c.E],[c.E,c.E,c.O]],
          [[c.X,c.O,c.E],[c.E,c.X,c.E],[c.O,c.E,c.E]]]

tester = c.Performance()

for board in boards:
    print(f'Test {boards.index(board) + 1}\nBefore algorithms')
    ttt.print_board(board)
    print('Minimax')
    optimal_move = minimax(board, tester)
    ttt.print_board(ttt.resultant(board, optimal_move))
    print(f'Time: {tester.prev_elapsed_time}')
    print('MCST')
    optimal_move = mcts(board, tester)
    ttt.print_board(ttt.resultant(board, optimal_move))
    print(f'Time: {tester.prev_elapsed_time}')