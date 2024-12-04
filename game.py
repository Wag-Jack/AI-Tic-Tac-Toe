import time
import tictactoe as ttt
import constants as c
from minimax import minimax

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

    b = ttt.Board()
    b.print_board()

    while not b.terminal():
        turn = b.current_player()
        print(f'{turn}\'S TURN!')

        if turn == c.X: #Human turn
            valid_move = False
            while not valid_move:
                x = int(input("Choose row: "))
                y = int(input("Choose column: "))

                if b.valid_move(x, y):
                    valid_move = True
                    b.set_space(turn, x, y)
                    b.print_board()
                else:
                    print("Invalid move, please try again.")
        
        else: # AI turn
            ai_move = minimax(b)
            b.set_space(turn, ai_move[0], ai_move[1])
            b.print_board()

        print()

    result = b.result()
    
    if result == 1:
        print("Human player wins!")
    elif result == -1:
        print("Computer player wins!")
    else:
        print("Tie!")
