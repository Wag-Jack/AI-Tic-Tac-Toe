import time

import tictactoe as ttt
import constants as c

from minimax import minimax
from mcts import mcts

def game(mode):
    match mode:
        case 1:
            #opponent = minimax
            print('',end='')
        case 2:
            #opponent = minimax
            print('',end='')
        case _:
            #error
            print('',end='')

    b = ttt.initial()
    ttt.print_board(b)

    while not ttt.terminal(b):
        turn = ttt.current_player(b)
        print(f'{turn}\'S TURN!')

        if turn == c.X: #Human turn
            valid_move = False
            while not valid_move:
                try:
                    x = int(input("Choose row: "))
                    y = int(input("Choose column: "))

                    if ttt.valid_move(b, x, y):
                        valid_move = True
                        b[x][y] = turn
                        ttt.print_board(b)
                    else:
                        print("Invalid move, please try again.")
                except ValueError:
                    print('Invalid input, please input a valid move.')
        
        else: # AI turn
            null = c.Performance()
            if mode == 1:
                ai_move = minimax(b, null)
            else:
                ai_move = mcts(b, null)
            
            b[ai_move[0]][ai_move[1]] = turn
            ttt.print_board(b)

        print()

    result = ttt.result(b)
    
    if result == 1:
        print("Human player wins!")
    elif result == -1:
        print("Computer player wins!")
    else:
        print("Tie!")