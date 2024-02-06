#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify

from api.v1.views import app_views

from models import storage

from models.amenity import Amenity

from models.city import City

from models.place import Place

from models.review import Review

from models.state import State

from models.user import User


@app_views.route('/status')
def get_status():
    '''Getting the status thats of the API.
    '''
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    '''
    Getting the number of the objects thats for each of the type.
    '''
    objjects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for keyy, valluee in objjects.items():
        objjects[keyy] = storage.count(valluee)
    return jsonify(objjects)
