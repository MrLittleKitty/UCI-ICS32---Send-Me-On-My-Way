import connectfour as connectfour
import connectfour_library as lib
import connectfour_protocol as network


def start_game() -> None:
    """
    The main entry point for the program.
    Starts the game of Connect Four.
    """
    print("Welcome to ICS 32 Connect Four!")
    host, port = get_address_and_port()
    username = get_username()

    if not network.connect_to_game_server(host, port, username):
        print('A connection could not be established with the server')
        return

    print('Successfully connected to the server. Ready to begin the game.')
    print('')
    gameState = connectfour.new_game()

    while connectfour.winner(gameState) == connectfour.NONE:
        if gameState.turn == connectfour.RED:
            lib.print_game_state(gameState)
            print('')
            while True:
                col, move = lib.prompt_and_get_move(gameState)
                response = network.send_move(move, col)
                if response == network.TERMINATED:
                    connection_terminated()
                    return
                elif response == network.ILLEGAL:
                    print("Invalid move. Try again.")
                else:
                    gameState = lib.execute_move(gameState, col, move)
                    break
        else:
            continue

    winner = connectfour.winner(gameState)
    print()
    lib.print_game_state(gameState)
    print(lib.get_player_string(winner) + ' has won the game! Congrats!')
    network.terminate_connection()
    return


def connection_terminated() -> None:
    ''' '''
    print('The connection to the server was terminated')


def get_username() -> str:
    while True:
        print("Please enter your username (without spaces)")
        username = input().strip()
        if ' ' not in username:
            return username


def get_address_and_port() -> (str, str):
    print("Please enter an IP address or host to connect to")
    host = input().strip()
    print("Please enter a port to connect to on the given host")
    port = input()
    return host, port


if __name__ == '__main__':
    start_game()
