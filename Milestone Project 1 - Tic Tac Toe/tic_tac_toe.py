board = [
    [-1, 0, 0],
    [0, 0, 0],
    [0, 1, 0],    
]

turn = 1

def get_char(value):
    if value == -1:
        return 'O'
    elif value == 1:
        return 'X'
    else:
        return ' '

def print_board():
    for row in board:
        print '+-+-+-+'
        print '|{0}|{1}|{2}|\t\ta b c'.format(get_char(row[0]), get_char(row[1]), get_char(row[2]))
    print '+-+-+-+'
    print 'Player {0}, where do you want to place your token (1-9)?'.format(get_char(turn))
    print

def main():
    print_board()

if __name__ == '__main__':
    main()
