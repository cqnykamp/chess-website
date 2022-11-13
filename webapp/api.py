'''
Charles Nykamp and Barry Nwike
Carleton College Software Design Class, Fall 2022
'''


import sys
import flask
import json
import psycopg2
import chess
import config

api = flask.Blueprint('api', __name__)



def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)


@api.route('/gameslist', strict_slashes=False)
def get_games_list():

    query = '''
        SELECT users_white.username, users_black.username
        FROM games
        LEFT OUTER JOIN users AS users_white
        ON users_white.id = games.white_player_id
        LEFT OUTER JOIN users AS users_black
        ON users_black.id = games.black_player_id
        LIMIT 10;
    '''

    games_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            game = {'white_username': row[0],
                      'black_username': row[1]}
            games_list.append(game)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(games_list)


@api.route('/game/<game_id>/')
def get_game(game_id):

    query = '''
        SELECT users_white.username, games.white_player_rating, users_black.username, games.black_player_rating, games.turns, games.victory_status, games.winner, games.rated_status, games.moves, openings.opening_name, games.increment_code
        FROM games
        LEFT OUTER JOIN users AS users_white
        ON users_white.id = games.white_player_id
        LEFT OUTER JOIN users AS users_black
        ON users_black.id = games.black_player_id
        LEFT OUTER JOIN openings
        ON openings.id = games.opening_id
        WHERE games.id = %s;
    '''

    game_data = {}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (game_id,))


        result = cursor.fetchone()
        if result:
            [white_username, white_rating, black_username, black_rating, turns, victory_status, winner, rated_status, moves, opening_name, increment_code] = result

            board = chess.Board()
            board_positions = []
            captured = []

            board_positions.append(str(board).replace(" ", "").replace('\n', "/"))
            captured = []

            for move_string in moves.split(" "):
                move = board.parse_san(move_string)
                print(f"Move is ${move}")

                captured_piece = ""
                if board.is_capture(move):
                    captured_piece = board.piece_at(move.to_square).symbol()

                board.push(move)
                # board.push_san(move_string)
                board_positions.append(str(board).replace(" ", "").replace('\n', "/"))
                captured.append(captured_piece)


            game_data = {
                'white_username': white_username,
                'white_rating': white_rating,
                'black_username': black_username,
                'black_rating': black_rating,
                'turns': turns,
                'victory_status': victory_status,
                'winner': winner,
                'rated_status': rated_status,
                'moves': moves,
                'opening_name': opening_name,
                'increment_code': increment_code,

                'board_positions': board_positions,
                'captured_pieces': captured,
            }
        else:
            print('There is no game for this id')

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(game_data)


@api.route('/help/')
def help():
    return flask.send_file('./doc/api-design.txt')