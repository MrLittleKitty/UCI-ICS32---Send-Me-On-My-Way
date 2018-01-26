import connectfour as lib


def print_game_state(state: lib.GameState) -> None:
    """
    Prints the contents of the given GameState to the console in a human readable way
    :param state: The GameState that will be printed to the console
    """
    for rowIdx in range(lib.BOARD_ROWS):
        for colIdx in range(lib.BOARD_COLUMNS):
            if colIdx == 0:
                print(str(state.board[colIdx][rowIdx]), end='')
            else:
                print(' ' + str(state.board[colIdx][rowIdx]), end='')
        print('')
