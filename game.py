import tictactoe as ttt
import constants as c

def game(mode):
    b = ttt.Board()
    b.print_board()

    while not b.terminal():
        turn = b.current_player()
        print(f'{turn}\'S TURN!')

        valid_move = False
        while not valid_move:
            x = int(input("Choose x position: "))
            y = int(input("Choose y position: "))

            if c.in_bounds(x, y):
                valid_move = True
                b.set_space(turn, y, x)
                b.print_board()
            else:
                print("Invalid move, please try again.")

    result = b.result()
    
    if result == 1:
        print("Human player wins!")
    elif result == -1:
        print("Computer player wins!")
    else:
        print("Tie!")
