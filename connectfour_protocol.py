import socket as socket
import connectfour as connectfour
import connectfour_library as lib

client_end_of_line = '\r\n'
server_end_of_line = '\n'
connection = None
in_stream = None
out_stream = None

drop = 'DROP'
pop = 'POP'

SUCCESS = 'OKAY'
ILLEGAL = 'INVALID'
WINNER_RED = 'WINNER_RED'
WINNDER_YELLOW = 'WINNER_YELLOW'


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
    except OSError as error:
        return False


def send_move(type: str, col: int) -> str:
    if type == lib.DROP_TOP:
        write_stream(drop + client_end_of_line)
    elif type == lib.POP_BOTTOM:
        write_stream(pop + client_end_of_line)

    global in_stream
    response = in_stream.readLine()


def write_stream(text: str) -> None:
    """

    :param text:
    :return:
    """
    global out_stream
    out_stream.write(text)
    out_stream.flush()
