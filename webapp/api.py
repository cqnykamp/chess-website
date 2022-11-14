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


@api.route('/games', strict_slashes=False)
def get_games_list():

    args = flask.request.args
    # print(args)

    query = '''
        SELECT games.id, users_white.username, games.white_player_rating, users_black.username, games.black_player_rating,
        games.turns, games.victory_status, games.winner, games.rated_status, openings.opening_name, games.increment_code
        FROM games
        LEFT OUTER JOIN users AS users_white
        ON users_white.id = games.white_player_id
        LEFT OUTER JOIN users AS users_black
        ON users_black.id = games.black_player_id
        LEFT OUTER JOIN openings
        ON openings.id = games.opening_id
        WHERE 1 = 1
    '''

    db_args = []

    if 'user' in args:
        query += '''
            AND (users_white.username ILIKE CONCAT(%s, '%%') OR users_black.username ILIKE CONCAT(%s, '%%'))
        '''
        db_args.append(args['user'])
        db_args.append(args['user'])


    if 'turns' in args:
        query += '''
            AND games.turns = %s
        '''
        db_args.append(args['turns'])


    if 'rating_max' in args:
        query += '''
            AND games.white_player_rating <= %s AND games.black_player_rating <= %s
        '''
        db_args.append(args['rating_max'])
        db_args.append(args['rating_max'])


    if 'rating_min' in args:
        query += '''
            AND (games.white_player_rating >= %s OR games.black_player_rating >= %s)
        '''
        db_args.append(args['rating_min'])
        db_args.append(args['rating_min'])

    if 'opening_moves' in args:
        query += '''
            AND REPLACE(games.moves, ' ', '-') ILIKE CONCAT(%s, '%%')
        '''
        db_args.append(args['opening_moves'])
    

    query += '''
        ORDER BY CASE WHEN games.white_player_rating > games.black_player_rating
            THEN games.white_player_rating
            ELSE games.black_player_rating
        END DESC
    '''


    if ('page_id' in args and args['page_id'].isdigit()) or ('page_size' in args and args['page_size'].isdigit()):

        # defaults
        page_size = 25
        page_id = 0

        try:
            page_size = int(args['page_size'])
        except:
            pass

        try:
            page_id = int(args['page_id'])
        except:
            pass

        # print('page size is ', page_size)
        # print(type(page_size))
        # print('page id is', page_id)
        # print(type(page_id))

        query += '''
            LIMIT %s OFFSET %s
        '''
        db_args.append(page_size)
        db_args.append(page_id * page_size)


    query += ";"


    print(query)


    games_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple(db_args))
        for row in cursor:

            [game_id, white_username, white_rating, black_username, black_rating, turns, victory_status, winner, rated_status, opening_name, increment_code] = row

            game_metadata = {
                'game_id': game_id,
                'white_username': white_username,
                'white_rating': white_rating,
                'black_username': black_username,
                'black_rating': black_rating,
                'turns': turns,
                'victory_status': victory_status,
                'winner': winner,
                'rated_status': rated_status,
                'opening_name': opening_name,
                'increment_code': increment_code,
            }

            games_list.append(game_metadata)
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

            print(moves)

            for move_string in moves.split(" "):
                move = board.parse_san(move_string)
                # print(f"Move is {move}")

                captured_piece_type = ""
                if board.is_capture(move):
                
                    to_square = move.to_square

                    if board.is_en_passant(move):
                        # Ensure that to_square points to the position of the captured piece
                        if to_square < 32:
                            to_square += 8
                        else:
                            to_square -= 8

                    captured_piece_type = board.piece_at(to_square).symbol()

                board.push(move)
                board_positions.append(str(board).replace(" ", "").replace('\n', "/"))
                captured.append(captured_piece_type)


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