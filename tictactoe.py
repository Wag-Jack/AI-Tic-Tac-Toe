import constants as c
import copy
import time

def initial():
    return [[c.E,c.E,c.E],
            [c.E,c.E,c.E],
            [c.E,c.E,c.E]]

def valid_move(board, row, col):
    if c.in_bounds(row,col) and board[row][col] == c.E:
        return True
    else:
        return False
    
def print_board(board):
    for row in range(3):
        print('+-+-+-+')
        print('|', end='')
        for col in range(3):
            print(f'{board[row][col]}|', end='')
        print()
    print('+-+-+-+')

def current_player(board):
    if board == initial():
        return c.X
    else:
        x_turns = 0
        o_turns = 0

        for row in range(3):
            for col in range(3):
                if board[row][col] == c.X:
                    x_turns += 1
                elif board[row][col] == c.O:
                    o_turns += 1
                
        if x_turns == o_turns:
            return c.X
        else:
            return c.O
        
def current_opponent(board):
    if board == terminal(board):
        return None
    else:
        x_turns = 0
        o_turns = 0

        for row in range(3):
            for col in range(3):
                if board[row][col] == c.X:
                    x_turns += 1
                elif board[row][col] == c.O:
                    o_turns += 1
        
        if x_turns == o_turns:
            return c.O
        else:
            return c.X

def actions(board):
    actions = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == c.E:
                actions.add((row,col))

    return actions

def resultant(board, action):
    resultant = copy.deepcopy(board)

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

        for ca in cases:
            for condition in win_conditions:
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

def terminal(board):
    if winner_found(board) == None:
        for row in range(3):
            for col in range(3):
                if board[row][col] == c.E:
                    return False
                
    return True

def result(board):
    result = winner_found(board)
        
    if result == c.X:
        return 1 #Human wins
    elif result == c.O:
        return -1 #AI wins
    else:
        return 0 #Tie