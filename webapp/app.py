'''
Charles Nykamp and Barry Nwike
Carleton College Software Design Class, Fall 2022
'''


import flask
import api
import argparse
import json


app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/game/<game_id>/')
def game(game_id):

    game_data = json.loads(api.get_game(game_id))

    # game_data = {
    #     'white_username': 'asdfadsf',
    #     'white_rating': 12345,
    #     'black_username': 'theBestChessPlayerEver',
    #     'black_rating': 600,
    #     'moves': "a1 b2 c3 Qxa4+",
    #     'winner': 'black',
    #     'victory_status': 'outoftime',
    #     'turns': 4,
    # }

    if 'moves' in game_data:
        # We assume that there is a game with this id
        return flask.render_template('game.html', game_data=game_data)
    else:
        return flask.render_template('no_game_found.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Analychess backend')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
