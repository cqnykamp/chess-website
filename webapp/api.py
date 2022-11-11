'''
Charles Nykamp and Barry Nwike
Carleton College Software Design Class, Fall 2022
'''


import sys
import flask
import json
import psycopg2
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
        SELECT users_white.username, users_black.username, games.moves
        FROM games
        LEFT OUTER JOIN users AS users_white
        ON users_white.id = games.white_player_id
        LEFT OUTER JOIN users AS users_black
        ON users_black.id = games.black_player_id
        WHERE games.id = %s;
    '''

    game_data = {}
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (game_id,))

        
        result = cursor.fetchone()
        if result:
            [white_username, black_username, moves] = result
            game_data = {
                'white_username': white_username,
                'black_username': black_username,
                'moves': moves,
            }
        else:
            print('There is no game for this id')

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(game_data)

