board = [0] * 9

turn = 1

def get_char(value):
    if value == -1:
        return 'O'
    elif value == 1:
        return 'X'
    else:
        return ' '

def get_winnable_lists_indices():
    # Return the lists that if all O's or all X's constitute a win.
    return [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

def print_board():
    for row in xrange(3):
        print '+-+-+-+'
        board_line = '|' + '|'.join([get_char(board[(row * 3) + col]) for col in xrange(3)]) + '|'
        board_line += '   ' + ' '.join([str((row * 3) + col + 1) for col in xrange(3)])
        print board_line
    print '+-+-+-+'
    print 'Player {0}, where do you want to place your token (1-9)?'.format(get_char(turn))
    print get_winner()
    print

def get_winner():
    # Returns 'O', 'X' or None (no winner).
    #
    # This is probably _not_ the most efficient way to do this; it is meant to exercise map(),
    # reduce() and any().
    winnable_lists = map(lambda indices: [board[i] for i in indices], get_winnable_lists_indices())
    totals = map(lambda winnable_list: (reduce(lambda x, y: x + y, winnable_list)), winnable_lists)
    if any(map(lambda total: total == -3, totals)):
        return 'O'
    elif any(map(lambda total: total == 3, totals)):
        return 'X'
    else:
        return None

def main():
    print_board()
    board[4] = 1
    print_board()
    board[2] = 1
    print_board()
    board[6] = 1
    print_board()
    board[6] = -1
    print_board()
    board[0] = -1
    print_board()
    board[3] = -1
    print_board()

if __name__ == '__main__':
    main()
