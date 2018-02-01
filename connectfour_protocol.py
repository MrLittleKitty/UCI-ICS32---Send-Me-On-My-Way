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

    :param address:
    :param port:
    :param username:
    :return:
    """
    try:
        global connection
        global in_stream
        global out_stream
        connection = socket.create_connection((address, port))
        in_stream = connection.makefile('r')
        out_stream = connection.makefile('w')

        write_stream('I32CFSP_HELLO ' + username + client_end_of_line)

        response = in_stream.readline()
        if response[0:7] != 'WELCOME' or response[8:] != (username + server_end_of_line):
            return False

        write_stream('AI_GAME' + server_end_of_line)

        response = in_stream.readline()
        if response != ('READY' + server_end_of_line):
            return False

        return True
    except:
        terminate_connection()
        return False


def send_move(move: str, col: int) -> str:
    """

    :param move:
    :param col:
    :return:
    """
    try:
        if move == lib.DROP_TOP:
            write_stream(drop + ' ' + str(col) + client_end_of_line)
        elif move == lib.POP_BOTTOM:
            write_stream(pop + ' ' + str(col) + client_end_of_line)

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

    :return:
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


def write_stream(text: str) -> None:
    """

    :param text:
    :return:
    """
    global out_stream
    out_stream.write(text)
    out_stream.flush()


def terminate_connection() -> None:
    global out_stream
    global in_stream
    global connection

    out_stream.close()
    in_stream.close()
    connection.close()
