import connectfour as lib

DROP_TOP = -2
POP_BOTTOM = -3


def get_player_string(player: int) -> str:
    """
    Returns a string representation of the given player number
    :param player: An integer value representing a player
    :return: A string that represents the given player
    """
    if player == lib.YELLOW:
        return 'Yellow'
    elif player == lib.RED:
        return 'Red'
    else:
        return 'None'


def get_player_symbol(player: int) -> str:
    """
    Returns a single character representation of the given player number
    :param player: An integer value representing a player
    :return: A single character that represents the given player
    """
    if player == lib.YELLOW:
        return 'Y'
    elif player == lib.RED:
        return 'R'
    else:
        return '.'


def print_game_state(state: lib.GameState) -> None:
    """
    Prints the contents of the given GameState to the console in a human readable way
    :param state: The GameState that will be printed to the console
    """
    for rowIdx in range(lib.BOARD_ROWS):
        for colIdx in range(lib.BOARD_COLUMNS):
            if colIdx == 0:
                print(get_player_symbol(state.board[colIdx][rowIdx]), end='')
            else:
                print(' ' + get_player_symbol(state.board[colIdx][rowIdx]), end='')
        print('')


def prompt_and_get_move(state: lib.GameState) -> (int, str):
    """
    Prompts the current player to enter a valid column number and a valid move type
    :param state: The current state of the game
    :return: A tuple whose first value is the entered column number and whose second value is the move type
    """
    print('It is the ' + get_player_string(state.turn) + ' players turn')
    while (True):
        print('Please input a column number (1-7) and a move (drop,pop). Example: 3 drop')
        line = input().strip()
        colString = line[0:1]
        move = line[2:]

        if not colString.isdigit():
            continue

        colNumber = int(colString)
        if colNumber < 1 or colNumber > 7:
            continue

        move = move.strip().lower()
        if move == 'drop':
            return colNumber - 1, DROP_TOP

        if move == 'pop':
            return colNumber - 1, POP_BOTTOM
