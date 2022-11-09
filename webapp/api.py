
import flask
import json

api = flask.Blueprint('api', __name__)

random_data = 'this is data from the server'

@api.route('/gameslist', strict_slashes=False)
def get_cats():
    return random_data
