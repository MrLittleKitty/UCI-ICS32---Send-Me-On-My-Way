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

    if not network.connect_to_game_server(host,port,username):
        print('A connection could not be established with the server')
        return

    print('Successfully connected to the server. Ready to begin the game.')
    gameState = connectfour.new_game()
    network.send_move(lib.DROP_TOP,1)

    return


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
