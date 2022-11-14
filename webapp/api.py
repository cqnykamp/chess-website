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
import chess_util

api = flask.Blueprint('api', __name__)



def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)



GAME_METADATA_FIELDS = '''
    users_white.username, games.white_player_rating, users_black.username, games.black_player_rating,
    games.turns, games.victory_status, games.winner, games.rated_status, games.increment_code,
    openings1.opening_name, openings2.opening_name, openings3.opening_name, openings4.opening_name,
    games.checks, games.captures, games.en_passants, games.castles, games.promotions
'''

GAME_METADATA_TABLE_JOINS = '''
    LEFT OUTER JOIN users AS users_white
    ON users_white.id = games.white_player_id
    LEFT OUTER JOIN users AS users_black
    ON users_black.id = games.black_player_id

    LEFT OUTER JOIN openings AS openings1
    ON openings1.id = games.opening1
    LEFT OUTER JOIN openings AS openings2
    ON openings2.id = games.opening2
    LEFT OUTER JOIN openings AS openings3
    ON openings3.id = games.opening3
    LEFT OUTER JOIN openings AS openings4
    ON openings4.id = games.opening4
'''


def package_metadata_row(metadata_row):
    [white_username, white_rating, black_username, black_rating, \
        turns, victory_status, winner, rated_status, increment_code, \
        opening1, opening2, opening3, opening4, \
        checks, captures, en_passants, castles, promotions \
    ] = metadata_row

    openings = []
    if opening1:
        openings.append(opening1)
    if opening2:
        openings.append(opening2)
    if opening3:
        openings.append(opening3)
    if opening4:
        openings.append(opening4)

    return {
        'white_username': white_username,
        'white_rating': white_rating,
        'black_username': black_username,
        'black_rating': black_rating,
        'turns': turns,
        'victory_status': victory_status,
        'winner': winner,
        'rated_status': rated_status,
        'opening_names': openings,
        'increment_code': increment_code,
    }



@api.route('/games', strict_slashes=False)
def get_games_list():

    args = flask.request.args
    # print(args)

    query = f'''
        SELECT games.id, { GAME_METADATA_FIELDS }
        FROM games
        { GAME_METADATA_TABLE_JOINS }
        WHERE 1 = 1
    '''


    db_args = []

    if 'user' in args:
        query += '''
            AND (users_white.username ILIKE CONCAT('%%', %s, '%%') OR users_black.username ILIKE CONCAT(%s, '%%'))
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

            # Create the JSON object and add it to the JSON list
            common_game_metadata = row[1:]
            game_metadata = package_metadata_row(common_game_metadata)
            game_metadata['game_id'] = row[0]
            games_list.append(game_metadata)

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(games_list)


@api.route('/game/<game_id>/')
def get_game(game_id):

    query = f'''
        SELECT games.moves, { GAME_METADATA_FIELDS }
        FROM games
        { GAME_METADATA_TABLE_JOINS}
        WHERE games.id = %s;
    '''

    game_data = {}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (game_id,))


        result = cursor.fetchone()
        if result:

            moves = result[0]

            # Generate board positions and captured pieces for each turn, from the list of moves

            board = chess.Board()
            board_positions = []
            captured = []

            board_positions.append(str(board).replace(" ", "").replace('\n', "/"))
            captured = []

            # print(moves)
            for move_string in moves.split(" "):
                move = board.parse_san(move_string)
                # print(f"Move is {move}")

                piece_type = chess_util.captured_piece_type(board, move)
                if piece_type == None:
                    piece_type = ""

                board.push(move)
                board_positions.append(str(board).replace(" ", "").replace('\n', "/"))
                captured.append(piece_type)


            # Create the JSON object
            game_data = package_metadata_row(result[1:])
            game_data['moves'] = moves
            game_data['board_positions'] = board_positions
            game_data['captured_pieces'] = captured

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