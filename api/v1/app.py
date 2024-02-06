#!/usr/bin/python3
'''
Contains a Flask web application API.
'''
import os

from models import storage

from flask import jsonify, Flask

from flask_cors import CORS

from api.v1.views import app_views


apps = Flask(__name__)
'''The Flask web application instance.'''
apps_hostt = os.getenv('HBNB_API_HOST', '0.0.0.0')
apps_portt = int(os.getenv('HBNB_API_PORT', '5000'))
apps.url_map.strict_slashes = False
apps.register_blueprint(app_views)
CORS(apps, resources={'/*': {'origins': apps_hostt}})


@apps.teardown_appcontext
def teardown_flask(exception):
    '''The function for the Flask apps/request of the context
    end's event for listener.'''
    storage.close()


@apps.errorhandler(404)
def error_404(error):
    '''This function handles the error 404 HTTP error's code.'''
    return jsonify(error='Not found'), 404


@apps.errorhandler(400)
def error_400(error):
    '''This function that handles the error code 400 HTTP.'''
    msge = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msge = error.description
    return jsonify(error=msge), 400


if __name__ == '__main__':
    apps_hostt = os.getenv('HBNB_API_HOST', '0.0.0.0')
    apps_portt = int(os.getenv('HBNB_API_PORT', '5000'))
    apps.run(
        host=apps_hostt,
        port=apps_portt,
        threaded=True
    )
