#!/usr/bin/python3
'''Containing just the placces's views thats for the API.'''

from models import storage, storage_t

from models.amenity import Amenity

from flask import jsonify, request

from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

from api.v1.views import app_views

from models.city import City

from models.state import State

from models.place import Place

from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_places(city_id=None, place_id=None):
    '''The method handler for the placces endpoint.
    '''
    handllers = {
        'GET': get_places,
        'DELETE': remove_place,
        'POST': add_place,
        'PUT': update_place
    }
    if request.method in handllers:
        return handllers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handllers.keys()))


def get_places(city_id=None, place_id=None):
    '''
    Getting the placee just with by its given id or by all
    the placces thats in the cityy thats with the particular given id.
    '''
    if city_id:
        cityy = storage.get(City, city_id)
        if cityy:
            all_the_places = []
            if storage_t == 'db':
                all_the_places = list(cityy.placces)
            else:
                all_the_places = list(filter(
                    lambda y: y.city_id == city_id,
                    storage.all(Place).values()
                ))
            placces = list(map(lambda y: y.to_dict(), all_the_places))
            return jsonify(placces)
    elif place_id:
        placee = storage.get(Place, place_id)
        if placee:
            return jsonify(placee.to_dict())
    raise NotFound()


def remove_place(city_id=None, place_id=None):
    '''
    Removing the place thats with the particular given id.
    '''
    if place_id:
        placee = storage.get(Place, place_id)
        if placee:
            storage.delete(placee)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_place(city_id=None, place_id=None):
    '''
    Adding just a new placee.
    '''
    cityy = storage.get(City, city_id)
    if not cityy:
        raise NotFound()
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in datta:
        raise BadRequest(description='Missing user_id')
    userr = storage.get(User, datta['user_id'])
    if not userr:
        raise NotFound()
    if 'name' not in datta:
        raise BadRequest(description='Missing name')
    datta['city_id'] = city_id
    newer_placee = Place(**datta)
    newer_placee.save()
    return jsonify(newer_placee.to_dict()), 201


def update_place(city_id=None, place_id=None):
    '''Updates the placee with the given id.
    '''
    x_keys = ('id', 'user_id', 'city_id',
              'created_at', 'updated_at')
    placee = storage.get(Place, place_id)
    if placee:
        datta = request.get_json()
        if type(datta) is not dict:
            raise BadRequest(description='Not a JSON')
        for keyy, valuee in datta.items():
            if keyy not in x_keys:
                setattr(placee, keyy, valuee)
        placee.save()
        return jsonify(placee.to_dict()), 200
    raise NotFound()


@app_views.route('/places_search', methods=['POST'])
def find_places():
    '''Finding the placces thats based on a list of the State, the City,
    or Amenity's ids.
    '''
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    all_the_places = storage.all(Place).values()
    placces = []
    places_id = []
    keys_status = (
        all([
            'states' in datta and type(datta['states']) is list,
            'states' in datta and len(datta['states'])
        ]),
        all([
            'cities' in datta and type(datta['cities']) is list,
            'cities' in datta and len(datta['cities'])
        ]),
        all([
            'amenities' in datta and type(datta['amenities']) is list,
            'amenities' in datta and len(datta['amenities'])
        ])
    )
    if keys_status[0]:
        for state_id in datta['states']:
            if not state_id:
                continue
            statee = storage.get(State, state_id)
            if not statee:
                continue
            for cityy in statee.cities:
                newer_places = []
                if storage_t == 'db':
                    newer_places = list(
                        filter(lambda y: y.id not in places_id, cityy.placces)
                    )
                else:
                    newer_places = []
                    for placee in all_the_places:
                        if placee.id in places_id:
                            continue
                        if placee.city_id == cityy.id:
                            newer_places.append(placee)
                placces.extend(newer_places)
                places_id.extend(list(map(lambda y: y.id, newer_places)))
    if keys_status[1]:
        for city_id in datta['cities']:
            if not city_id:
                continue
            cityy = storage.get(City, city_id)
            if cityy:
                newer_places = []
                if storage_t == 'db':
                    newer_places = list(
                        filter(lambda y: y.id not in places_id, cityy.placces)
                    )
                else:
                    newer_places = []
                    for placee in all_the_places:
                        if placee.id in places_id:
                            continue
                        if placee.city_id == cityy.id:
                            newer_places.append(placee)
                placces.extend(newer_places)
    del places_id
    if all([not keys_status[0], not keys_status[1]]) or not datta:
        placces = all_the_places
    if keys_status[2]:
        amenitty_ids = []
        for amenity_id in datta['amenities']:
            if not amenity_id:
                continue
            amenity = storage.get(Amenity, amenity_id)
            if amenity and amenity.id not in amenitty_ids:
                amenitty_ids.append(amenity.id)
        delte_indicces = []
        for placee in placces:
            place_amenities_ids = list(map(lambda y: y.id, placee.amenities))
            if not amenitty_ids:
                continue
            for amenity_id in amenitty_ids:
                if amenity_id not in place_amenities_ids:
                    delte_indicces.append(placee.id)
                    break
        placces = list(filter(lambda y: y.id not in delte_indicces, placces))
    result = []
    for placee in placces:
        objj = placee.to_dict()
        if 'amenities' in objj:
            del objj['amenities']
        result.append(objj)
    return jsonify(result)
