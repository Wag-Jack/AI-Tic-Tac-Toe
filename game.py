#Imports
import tictactoe as ttt
import constants as c

from minimax import minimax
from mcts import mcts


def game(mode):
    #Initialize the game board
    b = ttt.initial()
    ttt.print_board(b)

    #Run this loop until a terminal state is found
    while not ttt.terminal(b):
        #Determine who the current player is
        turn = ttt.current_player(b)
        print(f'{turn}\'S TURN!')

        if turn == c.X: #Human turn
            #Boolean to ensure a valid input
            valid_move = False
            while not valid_move:
                try:
                    #Get row and column entry for desired move
                    x = int(input("Choose row: "))
                    y = int(input("Choose column: "))

                    #Ensure valid move was made
                    if ttt.valid_move(b, x, y):
                        #Execute the move if valid
                        valid_move = True
                        b[x][y] = turn
                        ttt.print_board(b)
                    else:
                        #Tell the user their move was invalid and try again
                        print("Invalid move, please try again.")
                except ValueError:
                    print('Invalid input, please input a valid move.')
       
        else: # AI turn
            #Ensures user's designated AI agent was chosen
            if mode == 1:
                ai_move = minimax(b)
            else:
                ai_move = mcts(b)
           
            #Apply the AI's move to the board
            b[ai_move[0]][ai_move[1]] = turn
            ttt.print_board(b)

        print()

    #Once terminal state received, determine result of the game
    result = ttt.result(b)
   
    #Print out result of the game to the user
    if result == 1:
        print("Human player wins!")
    elif result == -1:
        print("Computer player wins!")
    else:
        print("Tie!")