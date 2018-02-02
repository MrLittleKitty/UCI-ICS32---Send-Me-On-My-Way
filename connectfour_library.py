import connectfour as lib

DROP_TOP = 'DROP'
POP_BOTTOM = 'POP'


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


def execute_move(state: lib.GameState, col: int, move: str) -> lib.GameState:
    """

    :param state:
    :param col:
    :param move:
    :return:
    """
    if move == DROP_TOP:
        return lib.drop(state, col - 1)
    elif move == POP_BOTTOM:
        return lib.pop(state, col - 1)
    else:
        raise lib.InvalidMoveError()


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


def print_turn(state: lib.GameState) -> None:
    """

    :param state:
    :return:
    """
    print('It is the ' + get_player_string(state.turn) + ' players turn')


def prompt_and_get_move() -> (int, str):
    """
    Prompts the current player to enter a valid column number and a valid move type
    :return: A tuple whose first value is the entered column number and whose second value is the move type
    """
    while True:
        print('Please input a move (drop,pop) and acolumn number (1-7). Example: drop 3')
        line = input().strip()

        move = line[0:4].strip()
        colString = line[4:].strip()

        if not colString.isdigit():
            continue

        colNumber = int(colString)
        if colNumber < 1 or colNumber > 7:
            continue

        move = move.lower()
        if move == 'drop':
            return colNumber, DROP_TOP

        if move == 'pop':
            return colNumber, POP_BOTTOM
