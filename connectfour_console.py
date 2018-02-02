import connectfour as connect
import connectfour_library as lib


def start_game() -> None:
    """
    The main entry point for the program.
    Starts the game of Connect Four.
    """
    print("Welcome to ICS 32 Connect Four!")
    gameState = connect.new_game()
    while connect.winner(gameState) == connect.NONE:
        lib.print_game_state(gameState)
        print('')
        lib.print_turn(gameState)
        while True:
            col, move = lib.prompt_and_get_move()
            try:
                gameState = lib.execute_move(gameState, col, move)
                break
            except connect.InvalidMoveError:
                if move == lib.POP_BOTTOM:
                    print('Can not pop on the given column')
                else:
                    print('Can not drop on the given column')
    winner = connect.winner(gameState)
    print()
    lib.print_game_state(gameState)
    print(lib.get_player_string(winner) + ' has won the game! Congrats!')
    return


if __name__ == '__main__':
    start_game()
