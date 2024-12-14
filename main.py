#Imports
import game as g

#Function to print menu and get user choice
def menu():
    #Setup and print the menu
    border = '-----------------------------------------------\n'
    s1 = 'WELCOME TO TIC-TAC-TOE | Choose opponent type.\n'
    s2 = '1.) Mini-Max w/ Alpha-Beta Pruning\n'
    s3 = '2.) Monte Carlo Tree Search\n'
    s4 = '3.) Quit\n'
    inp = "Choice: "
    menu = border + s1 + s2 + s3 + s4 + border + inp
   
    #Get the user input
    return int(input(menu))

#Main loop
def main():
    #Run until user selects 3 ('Quit')
    while True:
        #Choose game mode / option based on user's menu input
        match menu():
            case 1:
                g.game(1)
            case 2:
                g.game(2)
            case 3:
                break
            case _: #In the event something other than 1-3 inputted
                print('Invalid input, please try again.')

#Main execution
if __name__ == '__main__':
    main()