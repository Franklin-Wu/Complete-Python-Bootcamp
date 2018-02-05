board = [0] * 9

turn = 1

def get_char(value):
    if value == -1:
        return 'O'
    elif value == 1:
        return 'X'
    else:
        return ' '

def print_board():
    for row in xrange(3):
        print '+-+-+-+'
        board_line = '|' + '|'.join([get_char(board[(row * 3) + col]) for col in xrange(3)]) + '|'
        board_line += '   ' + ' '.join([str((row * 3) + col + 1) for col in xrange(3)])
        print board_line
    print '+-+-+-+'
    print 'Player {0}, where do you want to place your token (1-9)?'.format(get_char(turn))
    print

def main():
    print_board()

if __name__ == '__main__':
    main()
