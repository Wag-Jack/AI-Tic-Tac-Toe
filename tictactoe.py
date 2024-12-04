import constants as c
import copy

class Board:
    def __init__(self):
        self.board = [[c.E,c.E,c.E],
                      [c.E,c.E,c.E],
                      [c.E,c.E,c.E]]
        
        self.turns = 0
        self.x_turns = 0
        self.o_turns = 0
        
    def valid_move(self, i, j):
        if c.in_bounds(i, j) and self.board[i][j] == c.E:
            return True
        else:
            return False

    def set_space(self, player, i, j):
        if self.board[i][j] == c.E:
           self.board[i][j] = player
           self.turns += 1
           if player == c.X:
               self.x_turns += 1
           else:
               self.o_turns += 1
            
    def get_space(self, i, j):
        return self.board[i][j]
    
    def print_board(self):
        for r in range(3):
            print('+-+-+-+')
            print('|', end='')
            for c in range(3):
                print(f'{self.board[r][c]}|', end='')
            print()
        print('+-+-+-+')

    def current_player(self):
        if self.x_turns == self.o_turns: #Assume that X goes first
            return c.X
        else:
            return c.O

    def actions(self):
        actions = set()
        for row in range(3):
            for col in range(3):
                #Include any empty spaces in actions
                if self.board[col][row] == c.E:
                    actions.add((row,col))

        return actions

    def resultant(self, action):
        resultant = Board()
        resultant.board = copy.deepcopy(self.board) # Generates deep copy of board
        next_input = self.current_player()

        row, col = action # Maps action to coordinate point on board

        # Maps next input to resultant board and returns the board
        resultant.board[row][col] = next_input
        resultant.turns = self.turns + 1

        if next_input == c.X:
            resultant.x_turns = self.x_turns + 1
            resultant.o_turns = self.o_turns
        else: #Next turn is O
            resultant.x_turns = self.x_turns
            resultant.o_turns = self.o_turns + 1

        return resultant

    def winner_found(self):
        #Set of win condition points in a tic tac toe game
        win_conditions = [[(0,0),(0,1),(0,2)], #column 0
                          [(1,0),(1,1),(1,2)], #column 1
                          [(2,0),(2,1),(2,2)], #column 2
                          [(0,0),(1,0),(2,0)], #row 0
                          [(1,0),(1,1),(2,1)], #row 1
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
                    if self.board[point[1]][point[0]] != ca:
                        condition_met = False
                        break

                #Return the winning player
                if condition_met:
                    return ca
                    
        return None #No one has won yet

    #Determines if the game has ended or not
    def terminal(self):
        if self.winner_found() == None:
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == c.E:
                        return False
                
        return True

    def result(self):
        result = self.winner_found()
        
        if result == None:
            return 0 #Tie
        elif result == c.O:
            return -1 #AI wins
        else:
            return 1 #Human wins