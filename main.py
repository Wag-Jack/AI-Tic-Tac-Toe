import game as g

def menu():
    border = '-----------------------------------------------\n'
    s1 = 'WELCOME TO TIC-TAC-TOE | Choose opponent type.\n'
    s2 = '1.) Mini-Max w/ Alpha-Beta Pruning\n'
    s3 = '2.) Monte Carlo Tree Search\n'
    s4 = '3.) Quit\n'
    inp = "Choice: "
    
    menu = border + s1 + s2 + s3 + s4 + border + inp 
    return int(input(menu))

def main():
    while True:
        match menu():
            case 1:
                g.game(1)
            case 2:
                g.game(2)
            case 3:
                break
            case _:
                print('Invalid input, please try again.')

if __name__ == '__main__':
    main()