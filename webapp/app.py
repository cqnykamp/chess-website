'''
Charles Nykamp and Barry Nwike
Carleton College Software Design Class, Fall 2022
'''


import flask
import api
import argparse


app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')


@app.route('/')
def home():
    return flask.render_template('index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Analychess backend')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
