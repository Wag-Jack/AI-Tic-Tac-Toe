import tictactoe as ttt

def game(mode):
    b = ttt.Board

    while b.winner_found() == None:
        turn = b.check_current_player()
        b.print_board()

        valid_move = False
        while not valid_move:
            x = int(input("Choose x position: "))
            y = int(input("Choose y position: "))

            if b.check_legal_move(x, y):
                valid_move = True
                b.set_space(turn, x, y)
            else:
                print("Invalid move, please try again.")
