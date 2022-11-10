
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
        SELECT white_player_id, black_player_id FROM games LIMIT 5;
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