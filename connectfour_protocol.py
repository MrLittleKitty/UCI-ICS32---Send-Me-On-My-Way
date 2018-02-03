# Eric Wolfe 76946154 eawolfe@uci.edu
import socket as socket
import connectfour_library as lib

client_end_of_line = '\r\n'
server_end_of_line = '\n'
connection = None
in_stream = None
out_stream = None

drop = 'DROP'
pop = 'POP'

SUCCESS = 'OKAY' + server_end_of_line
ILLEGAL = 'INVALID' + server_end_of_line
WINNER_RED = 'WINNER_RED' + server_end_of_line
WINNER_YELLOW = 'WINNER_YELLOW' + server_end_of_line
TERMINATED = 'TERMINATED'


def connect_to_game_server(address: str, port: str, username: str) -> bool:
    """
    Attempts to connect to a connect four game server at the given host address and host port
    :param address: The host address to attempt the connection to
    :param port: The host port that the connection should go through
    :param username: The username to use when connecting to the game server
    :return: True if the connection was successful and the game is ready to be played. False otherwise
    """
    try:
        global connection
        global in_stream
        global out_stream
        connection = socket.create_connection((address, port))
        in_stream = connection.makefile('r')
        out_stream = connection.makefile('w')

        _write_stream('I32CFSP_HELLO ' + username + client_end_of_line)

        response = in_stream.readline()
        if response[0:7] != 'WELCOME' or response[8:] != (username + server_end_of_line):
            return False

        _write_stream('AI_GAME' + server_end_of_line)

        response = in_stream.readline()
        if response != ('READY' + server_end_of_line):
            return False

        return True
    except:
        terminate_connection()
        return False


def send_move(move: str, col: int) -> str:
    """
    Sends the given move on the given column to the connected game server
    :param move: The move that will be sent to the connected game server
    :param col: The column that the move will be executed on
    :return: The response from the game server (TERMINATED, SUCCESS, ILLEGAL, WINNER_RED, WINNER_YELLOW)
    """
    try:
        if move == lib.DROP_TOP:
            _write_stream(drop + ' ' + str(col) + client_end_of_line)
        elif move == lib.POP_BOTTOM:
            _write_stream(pop + ' ' + str(col) + client_end_of_line)

        global in_stream
        response = in_stream.readline()

        if response == ILLEGAL:
            response = in_stream.readline()
            if response != ('READY'+server_end_of_line):
                terminate_connection()
                return TERMINATED
            return ILLEGAL
        elif response != SUCCESS and response != WINNER_RED and response != WINNER_YELLOW:
            terminate_connection()
            return TERMINATED

        return response
    except:
        terminate_connection()
        return TERMINATED


def receive_move() -> (str, int) or TERMINATED:
    """
    Receives the other player's move from connected game server.
    :return: Either a tuple whose first value is the move type and whose second value is the column OR TERMINATED.
    """
    try:
        global in_stream
        response = in_stream.readline()
        move = None
        col = None
        if response[0:4] == 'DROP':
            move = lib.DROP_TOP
            value = response[5:].strip()
            col = int(value)
        elif response[0:3] == 'POP':
            move = lib.POP_BOTTOM
            value = response[4:].strip()
            col = int(value)
        else:
            terminate_connection()
            return TERMINATED

        response = in_stream.readline()
        if response == WINNER_RED or response == WINNER_YELLOW:
            terminate_connection()
        elif response != ('READY'+server_end_of_line):
            terminate_connection()
            return TERMINATED

        return move, col
    except:
        terminate_connection()
        return TERMINATED


def _write_stream(text: str) -> None:
    """
    Writes the given text to the network output stream and then flushes the stream
    :param text: The text that will be written to the output stream
    """
    global out_stream
    out_stream.write(text)
    out_stream.flush()


def terminate_connection() -> None:
    """Closes the network connection and closes all related streams"""
    global out_stream
    global in_stream
    global connection

    out_stream.close()
    in_stream.close()
    connection.close()
