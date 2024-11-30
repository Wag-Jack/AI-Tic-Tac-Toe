import tictactoe as ttt
import constants as c

def game(mode):
    b = ttt.Board()

    state = None
    while state == None:
        turn = b.current_player()
        b.print_board()

        valid_move = False
        while not valid_move:
            x = int(input("Choose x position: "))
            y = int(input("Choose y position: "))

            if c.in_bounds(x, y):
                valid_move = True
                b.set_space(turn, x, y)
            else:
                print("Invalid move, please try again.")

        state = b.result()

    if state == c.X:
        print("Human player wins!")
    elif state == c.O:
        print("Computer player wins!")
    else:
        print("Tie!")
