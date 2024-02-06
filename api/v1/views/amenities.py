#!/usr/bin/python3
'''Containing just the amenities views thats for the API.'''

from models import storage

from models.amenity import Amenity

from flask import jsonify, request

from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

from api.v1.views import app_views


ALLOWED_METHODS = ['GET', 'POST', 'DELETE', 'PUT']
'''Methods that are allowed just for the amenitie's endpoint.'''


@app_views.route('/amenities', methods=ALLOWED_METHODS)

@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    '''
    This function  is a method for handler for the amenitie's endpoint.
    '''
    handdlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handdlers:
        return handdlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handdlers.keys()))


def get_amenities(amenity_id=None):
    '''
    Getting the amenity just with by its given id or by all
    the amenities.
    '''
    all_the_amenities = storage.all(Amenity).values()
    if amenity_id:
        ress = list(filter(lambda y: y.id == amenity_id, all_the_amenities))
        if ress:
            return jsonify(ress[0].to_dict())
        raise NotFound()
    all_the_amenities = list(map(lambda y: y.to_dict(), all_the_amenities))
    return jsonify(all_the_amenities)


def remove_amenity(amenity_id=None):
    '''
    Removing the amenity thats with the given id.
    '''
    all_the_amenities = storage.all(Amenity).values()
    ress = list(filter(lambda y: y.id == amenity_id, all_the_amenities))
    if ress:
        storage.delete(ress[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''
    Adding just a new amenity.
    '''
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in datta:
        raise BadRequest(description='Missing name')
    neww_ammenity = Amenity(**datta)
    neww_ammenity.save()
    return jsonify(neww_ammenity.to_dict()), 201


def update_amenity(amenity_id=None):
    '''
    Updating the amenity thats with the given id.
    '''
    x_keys = ('id', 'created_at', 'updated_at')
    all_the_amenities = storage.all(Amenity).values()
    ress = list(filter(lambda y: y.id == amenity_id, all_the_amenities))
    if ress:
        datta = request.get_json()
        if type(datta) is not dict:
            raise BadRequest(description='Not a JSON')
        oldd_amenityy = ress[0]
        for key, value in datta.items():
            if key not in x_keys:
                setattr(oldd_amenityy, key, value)
        oldd_amenityy.save()
        return jsonify(oldd_amenityy.to_dict()), 200
    raise NotFound()
