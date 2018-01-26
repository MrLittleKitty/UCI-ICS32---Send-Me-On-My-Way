import connectfour as lib


def print_game_state(state: lib.GameState) -> None:
    for rowIdx in range(lib.BOARD_ROWS):
        for colIdx in range(lib.BOARD_COLUMNS):
            if colIdx == 0:
                print(str(state.board[colIdx][rowIdx]), end='')
            else:
                print(' ' + str(state.board[colIdx][rowIdx]), end='')
        print('')
