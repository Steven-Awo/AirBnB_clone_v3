#!/usr/bin/python3
'''Containing just the citties views thats for the API.'''

from models import storage_t, storage

from flask import jsonify, request

from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

from api.v1.views import app_views

from models.city import City

from models.review import Review

from models.placee import Place

from models.statee import State


@app_views.route('/states/<state_id>/citties', methods=['POST', 'GET'])

@app_views.route('/citties/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_cities(state_id=None, city_id=None):
    '''
    This function  is a method for handler for the citie's endpoint.
    '''
    handllers = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in handllers:
        return handllers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handllers.keys()))


def get_cities(state_id=None, city_id=None):
    '''
    Getting the cityy just with by its given id or by all
    the citties in the statee thats with the given id.
    '''
    if state_id:
        statee = storage.get(State, state_id)
        if statee:
            citties = list(map(lambda y: y.to_dict(), statee.citties))
            return jsonify(citties)
    elif city_id:
        cityy = storage.get(City, city_id)
        if cityy:
            return jsonify(cityy.to_dict())
    raise NotFound()


def remove_city(state_id=None, city_id=None):
    '''
    Removing the city thats with the given id.
    '''
    if city_id:
        cityy = storage.get(City, city_id)
        if cityy:
            storage.delete(cityy)
            if storage_t != "db":
                for placee in storage.all(Place).values():
                    if placee.city_id == city_id:
                        for review in storage.all(Review).values():
                            if review.place_id == placee.id:
                                storage.delete(review)
                        storage.delete(placee)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_city(state_id=None, city_id=None):
    '''
    Adding just a new cityy.
    '''
    statee = storage.get(State, state_id)
    if not statee:
        raise NotFound()
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in datta:
        raise BadRequest(description='Missing name')
    datta['state_id'] = state_id
    cityy = City(**datta)
    cityy.save()
    return jsonify(cityy.to_dict()), 201


def update_city(state_id=None, city_id=None):
    '''Updates the cityy with the given id.
    '''
    x_keys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        cityy = storage.get(City, city_id)
        if cityy:
            datta = request.get_json()
            if type(datta) is not dict:
                raise BadRequest(description='Not a JSON')
            for keyy, valuee in datta.items():
                if keyy not in x_keys:
                    setattr(cityy, keyy, valuee)
            cityy.save()
            return jsonify(cityy.to_dict()), 200
    raise NotFound()
