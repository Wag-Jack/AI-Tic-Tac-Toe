#Imports
import copy

import constants as c

#Function to return initial, empty board state
def initial():
    return [[c.E,c.E,c.E],
            [c.E,c.E,c.E],
            [c.E,c.E,c.E]]

#Function to determine if move is valid on tic-tac-toe board
def valid_move(board, row, col):
    #Valid move is when 0 <= x <= 2 and 0 <= y <= 2
    #AND the requested board space is not empty
    if c.in_bounds(row,col) and board[row][col] == c.E:
        return True
    else:
        return False
   
#Function to print out the board in an organized fashion
def print_board(board):
    for row in range(3):
        #Start of row
        print('+-+-+-+')
        print('|', end='')
        #Start of column
        for col in range(3):
            print(f'{board[row][col]}|', end='')
        #End of column
        print()
        #End of row
    print('+-+-+-+')

#Function to determine the next player for the given board
def current_player(board):
    if board == initial():
        return c.X #initial state automatically means X's turn
    else:
        #Functions to keep track of the turns from each player
        x_turns = 0
        o_turns = 0

        #Iterate through the board and increment turn variables based on what player it is
        for row in range(3):
            for col in range(3):
                if board[row][col] == c.X:
                    x_turns += 1
                elif board[row][col] == c.O:
                    o_turns += 1
               
        #Determine next player
        if x_turns == o_turns:
            return c.X #Same turns means O has just went, X is next
        else:
            return c.O #X being one turn ahead means O is next
       
#Function to determine the player that is up next
def current_opponent(board):
    if board == terminal(board):
        return None #terminal state meeans no player is next
    else:
        #Functions to keep track of turns for each player
        x_turns = 0
        o_turns = 0

        #Iterate through the board and increment turn variables based on what player it is
        for row in range(3):
            for col in range(3):
                if board[row][col] == c.X:
                    x_turns += 1
                elif board[row][col] == c.O:
                    o_turns += 1
       
        #Determine next player
        if x_turns == o_turns:
            return c.O #Same turns means X is currently choosing, O is next
        else:
            return c.X #X being one turn ahead of O means X is in two turns

#Function to return all possible actions of the given board state
def actions(board):
    #Initialize empty set of actions
    actions = set()
   
    #Iterate through the board
    for row in range(3):
        for col in range(3):
            if board[row][col] == c.E:
                #Actions to take will be any board space that is empty
                actions.add((row,col))

    return actions

def resultant(board, action):
    #Create a deep copy of the current board to generate resultant state
    resultant = copy.deepcopy(board)

    #Apply the move to the resultant board
    row, col = action
    resultant[row][col] = current_player(board)

    return resultant

def winner_found(board):
    #Set of win condition points in a tic tac toe game
        win_conditions = [[(0,0),(0,1),(0,2)], #column 0
                          [(1,0),(1,1),(1,2)], #column 1
                          [(2,0),(2,1),(2,2)], #column 2
                          [(0,0),(1,0),(2,0)], #row 0
                          [(0,1),(1,1),(2,1)], #row 1
                          [(0,2),(1,2),(2,2)], #row 2
                          [(0,0),(1,1),(2,2)], #diagnol top left to bottom right
                          [(2,0),(1,1),(0,2)]] #diagnol top right to bottom left
           
        cases = [c.X, c.O]

        #Main loop checks the board with each player
        for ca in cases:
            #Check each possible win condition for validation
            for condition in win_conditions:
                #Boolean to ensure that valid condition is met
                condition_met = True
                for point in condition:
                    #If at least one position in the win condition does not match,
                    #that specific win condition was not met, so we stop iterating.
                    if board[point[0]][point[1]] != ca:
                        condition_met = False
                        break

                #Return the winning player
                if condition_met:
                    return ca
                   
        return None #No one has won yet

#Function to determine if the board is in a terminal state (finished playing)
def terminal(board):
    #Don't iterate through the board if we already have a winner
    if winner_found(board) == None:
        #Iterate through the board
        for row in range(3):
            for col in range(3):
                #If no winner and any space is empty, there are still moves to be made
                if board[row][col] == c.E:
                    return False
               
    #Either a winner was found or there are no more moves left
    return True

#Function to determine the result of the game
def result(board):
    #Get the actual result of who won or if there was a draw
    result = winner_found(board)
       
    #Convert result into a numerical value for adversarial search algorithms
    if result == c.X:
        return 1 #Human wins
    elif result == c.O:
        return -1 #AI wins
    else:
        return 0 #Tie