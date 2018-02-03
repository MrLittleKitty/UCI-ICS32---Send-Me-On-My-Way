# Eric Wolfe 76946154 eawolfe@uci.edu
import connectfour as connectfour
import connectfour_library as lib
import connectfour_protocol as network


def start_game() -> None:
    """
    The main entry point for the program.
    Starts the networked version of the connect four game.
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
            print('You are the Red player. It is your move.')
            while True:
                col, move = lib.prompt_and_get_move()
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
            lib.print_game_state(gameState)
            print('')
            move, col = network.receive_move()
            if move == network.TERMINATED:
                connection_terminated()
                return
            gameState = lib.execute_move(gameState, col, move)
            print('The Yellow player has made the move: ' + move + ' ' + str(col))

    winner = connectfour.winner(gameState)
    print()
    lib.print_game_state(gameState)
    print('')
    if winner == connectfour.RED:
        print('You have won the game! Congrats!')
    else:
        print('The Yellow player has won the game.')
    network.terminate_connection()
    return


def connection_terminated() -> None:
    """Calls the network handler to terminate the connection and prints a notification to the console"""
    network.terminate_connection()
    print('The connection to the server was terminated')


def get_username() -> str:
    """
    Prompts the user to enter a username and then returns it
    :return: The username entered by the user
    """
    while True:
        print("Please enter your username (without spaces)")
        username = input().strip()
        if ' ' not in username:
            return username


def get_address_and_port() -> (str, str):
    """
    Prompts the user to enter an address to connect to as well as a port
    :return: A tuple whose first value is the host address and whose second value is the host port
    """
    print("Please enter an IP address or host to connect to")
    host = input().strip()
    print("Please enter a port to connect to on the given host")
    port = input()
    return host, port


if __name__ == '__main__':
    start_game()
