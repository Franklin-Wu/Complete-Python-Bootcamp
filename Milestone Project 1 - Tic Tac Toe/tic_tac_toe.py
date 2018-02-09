board = [0] * 9
turn_player = 1
valid_positions = list('123456789')

def get_player_char(player):
    if player == -1:
        return 'O'
    elif player == 1:
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
        board_line = '|'
        board_line += '|'.join([get_player_char(board[(row * 3) + col]) for col in xrange(3)])
        board_line += '|   ' + ' '.join([str((row * 3) + col + 1) for col in xrange(3)])
        print board_line
    print '+-+-+-+'

def get_winning_player():
    # Returns 'O', 'X' or None (no winning player yet).
    #
    # This is probably _not_ the most efficient way to do this; it is meant to exercise map(),
    # reduce() and any().

    # Get the contents of each 3-cell row, column and diagonal.
    winnable_lists = map(lambda indices: [board[i] for i in indices], get_winnable_lists_indices())

    # Get the sums of each 3-cell row, column and diagonal.
    sums = map(lambda winnable_list: (reduce(lambda x, y: x + y, winnable_list)), winnable_lists)

    if any(map(lambda total: total == -3, sums)):
        # If any of the sums are -3, O wins.
        return -1
    elif any(map(lambda total: total == 3, sums)):
        # If any of the sums are -3, X wins.
        return 1
        # Otherwise nobody wins (yet).
    else:
        return None

def get_turn_player_input():
    player_char = get_player_char(turn_player)
    prompt = 'Player {0}, where do you place your token (1-9)? '.format(player_char)
    reminder_prompt = 'Invalid input; enter a digit from 1 to 9. '
    occupied_cell_prompt = 'Position {0} is occupied; try again. '
    s = raw_input(prompt)
    while True:
        # need to check for occupied cells
        if s in valid_positions:
            position = int(s)
            if board[position - 1] != 0:
                s = raw_input(occupied_cell_prompt.format(position))
            else:
                return position
        else:
            s = raw_input(reminder_prompt)

def play_turn():
    global turn_player
    print_board()
    position = get_turn_player_input()
    board[position - 1] = turn_player
    winning_player = get_winning_player()
    print
    turn_player *= -1
    return winning_player

def main():
    winning_player = None
    for turn in xrange(9):
        winning_player = play_turn()
        if winning_player:
            break
    print_board()
    if winning_player:
        print 'Player {0} wins the game.'.format(get_player_char(winning_player))
    else:
        print 'The game ends in a tie.'

if __name__ == '__main__':
    main()
