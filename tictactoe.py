import constants as c

class Board:
    def __init__(self):
        self.board = [[c.E,c.E,c.E],
                      [c.E,c.E,c.E],
                      [c.E,c.E,c.E]]
        
        self.turns = 0
        self.x_turns = 0
        self.o_turns = 0
        
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
            
        cases = [c.O, c.X]

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
            return 0
        elif result == c.O:
            return -1
        else:
            return 1