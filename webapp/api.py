
import flask
import json

api = flask.Blueprint('api', __name__)

sample_data = [
    {
        'white_username': 'avocado',
        'black_username': 'Terry',
    },
    {
        'white_username': 'totallyMagnusCarlsen',
        'black_username': 'mirco25',
    },

]


@api.route('/gameslist', strict_slashes=False)
def get_cats():
    return json.dumps(sample_data)