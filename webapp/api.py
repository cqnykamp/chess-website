"""
Charles Nykamp and Barry Nwike
Carleton College Software Design Class, Fall 2022

The API for querying the database about chess games
"""


import sys
import flask
import json
import psycopg2
import chess

import config
import chess_util

api = flask.Blueprint('api', __name__)



# Common database fields shared across multiple endpoint queries
GAME_METADATA_FIELDS = '''
    /* Players */
    users_white.username, games.white_player_rating, users_black.username, games.black_player_rating,

    /* Outcome */
    games.turns, games.victory_status, games.winner, games.rated_status, games.increment_code,

    /* Openings */
    openings1.opening_name, openings2.opening_name, openings3.opening_name, openings4.opening_name,

    /* Stats */
    games.checks, games.captures, games.en_passants, games.castles, games.promotions,

    /* Piece type specifics on captures */
    games.capturing_queens, games.capturing_rooks, games.capturing_bishops, games.capturing_knights, games.capturing_pawns, games.capturing_kings,
    games.captured_queens, games.captured_rooks, games.captured_bishops, games.captured_knights, games.captured_pawns

'''

# Common table joins shared across multiple endpoint queries
GAME_METADATA_TABLE_JOINS = '''
    /* Join white and black players as separate tables */
    LEFT OUTER JOIN users AS users_white
    ON users_white.id = games.white_player_id
    LEFT OUTER JOIN users AS users_black
    ON users_black.id = games.black_player_id

    /* Join all four possible opening names as separate tables */
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
    """Given one row of results from the `GAME_METADATA_FIELDS`, package the fields
        nicely into a JSON object, with some minor formatting """

    # Unpack the GAME_METADATA_FIELDS values
    [ \
        # Players
        white_username, white_rating, black_username, black_rating, \
        # Outcome
        turns, victory_status, winner, rated_status, increment_code, \
        # Openings
        opening1, opening2, opening3, opening4, \
        # Stats
        checks, captures, en_passants, castles, promotions, \
        # Piece type specifics on captures
        capturing_queens, capturing_rooks, capturing_bishops, capturing_knights, capturing_pawns, capturing_kings, \
        captured_queens, captured_rooks, captured_bishops, captured_knights, captured_pawns, \

    ] = metadata_row

    # List of non-null openings for this row
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

        'checks': checks,
        'captures': captures,
        'en_passants': en_passants,
        'promotions': promotions,
        'captured_pieces': {
            'queen': captured_queens,
            'rook': captured_rooks,
            'knight': captured_knights,
            'bishop': captured_bishops,
            'pawn': captured_pawns,
        },
        'captures_by_piece': {
            'king': capturing_kings,
            'queen': capturing_queens,
            'rook': capturing_rooks,
            'knight': capturing_knights,
            'bishop': capturing_bishops,
            'pawn': capturing_pawns,
        }
    }


def get_connection():
    """ Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. """
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)



@api.route('/games', strict_slashes=False)
def get_games_list():
    """Generates a JSON list of games filtered by GET parameters"""


    args = flask.request.args

    query = f'''
        SELECT games.id,
        { GAME_METADATA_FIELDS }
        FROM games
        { GAME_METADATA_TABLE_JOINS }
        WHERE 1 = 1
    '''


    # The arguments passed into our SQL query when we execute it
    db_args = []


    if 'user' in args:
        # Filter by username or partial username of either player
        query += '''
            AND (users_white.username ILIKE CONCAT('%%', %s, '%%') OR users_black.username ILIKE CONCAT('%%', %s, '%%'))
        '''
        db_args.append(args['user'])
        db_args.append(args['user'])


    if 'turns' in args:
        # Filter by exact number of turns
        query += '''
            AND games.turns = %s
        '''
        db_args.append(args['turns'])


    if 'rating_max' in args:
        # Filter by maximum rating of both player
        query += '''
            AND games.white_player_rating <= %s AND games.black_player_rating <= %s
        '''
        db_args.append(args['rating_max'])
        db_args.append(args['rating_max'])


    if 'rating_min' in args:
        # Filter by minimum rating of one player
        query += '''
            AND (games.white_player_rating >= %s OR games.black_player_rating >= %s)
        '''
        db_args.append(args['rating_min'])
        db_args.append(args['rating_min'])


    if 'moves' in args:
        # Filter by moves
        query += '''
            AND games.moves ILIKE CONCAT('%%', %s, '%%')
        '''
        db_args.append(args['moves'])



    if 'opening_moves' in args:
        # Filter by opening moves
        query += '''
            AND games.moves ILIKE CONCAT(%s, '%%')
        '''
        db_args.append(args['opening_moves'])


    if 'opening_name' in args:
        # Filter by name of opening moves
        query += '''
            AND ( openings1.opening_name ILIKE CONCAT('%%', %s, '%%') OR openings2.opening_name ILIKE CONCAT('%%', %s, '%%')
                OR openings3.opening_name ILIKE CONCAT('%%', %s, '%%') OR openings4.opening_name ILIKE CONCAT('%%', %s, '%%') )
        '''
        db_args.append(args['opening_name'])
        db_args.append(args['opening_name'])
        db_args.append(args['opening_name'])
        db_args.append(args['opening_name'])
    

    # Sort the results by player rating descending
    query += '''
        ORDER BY CASE WHEN games.white_player_rating > games.black_player_rating
            THEN games.white_player_rating
            ELSE games.black_player_rating
        END DESC
    '''


    if ('page_id' in args and args['page_id'].isdigit()) or ('page_size' in args and args['page_size'].isdigit()):
        # If either page_id or page_size is specified, return only a page of results

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


        query += '''
            LIMIT %s OFFSET %s
        '''
        db_args.append(page_size)
        db_args.append(page_id * page_size)


    query += ";"
    # print(query)


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
    """Get the full game data of a particular game id.
        As well as returning the game metadata, this API endpoint returns the moves
        list, the board positions after every turn, and the type of piece captured
        after every turn. Some of this data is generated on each API call -- it is
        not stored in the database. """

    query = f'''
        SELECT games.moves,
        { GAME_METADATA_FIELDS }
        FROM games
        { GAME_METADATA_TABLE_JOINS}
        WHERE games.id = %s;
    '''

    game_data = {}
    try:
        # Connect to database and execute SQL query
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (game_id,))

        # Fetch only one row -- we're assuming that the SQL query outputs only one row anyway
        result = cursor.fetchone()

        if result:
            moves = result[0]

            # Generate board positions and captured pieces from the list of moves
            board = chess.Board()
            board_positions = []
            captured = []
            captured = []

            format_board = lambda x: str(x).replace(" ", "").replace('\n', "/")


            board_positions.append(format_board(board))
            for move_string in moves.split(" "):
                move = board.parse_san(move_string)

                piece_type = chess_util.captured_piece_type(board, move)
                if piece_type == None:
                    piece_type = ""

                board.push(move)
                board_positions.append(format_board(board))
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