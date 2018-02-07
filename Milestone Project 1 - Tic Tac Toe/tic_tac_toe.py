board = [0] * 9

turn_player = 1

def get_char(value):
    if value == -1:
        return 'O'
    elif value == 1:
        return 'X'
    else:
        return ' '

def get_winnable_lists_indices():
    # Return the lists that if all O's or all X's constitute a win, that is, the indices comprising
    # each 3-cell row, column and diagonal.
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

def get_winner():
    # Returns 'O', 'X' or None (no winner).
    #
    # This is probably _not_ the most efficient way to do this; it is meant to exercise map(),
    # reduce() and any().

    # Get the contents of each 3-cell row, column and diagonal.
    winnable_lists = map(lambda indices: [board[i] for i in indices], get_winnable_lists_indices())

    # Get the sums of each 3-cell row, column and diagonal.
    sums = map(lambda winnable_list: (reduce(lambda x, y: x + y, winnable_list)), winnable_lists)

    if any(map(lambda total: total == -3, sums)):
        # If any of the sums are -3, O wins.
        return 'O'
    elif any(map(lambda total: total == 3, sums)):
        # If any of the sums are -3, X wins.
        return 'X'
        # Otherwise nobody wins (yet).
    else:
        return None

def get_turn_player_input():
    pass

def play_turn():
    global turn_player
    print_board()
    print 'Player {0}, where do you want to place your token (1-9)?'.format(get_char(turn_player))
    winner = get_winner()
    print winner
    print
    turn_player *= -1
    return winner

def main():
    play_turn()
    board[4] = 1
    play_turn()
    board[2] = 1
    play_turn()
    board[6] = 1
    play_turn()
    board[6] = -1
    play_turn()
    board[0] = -1
    play_turn()
    board[3] = -1
    play_turn()

if __name__ == '__main__':
    main()
