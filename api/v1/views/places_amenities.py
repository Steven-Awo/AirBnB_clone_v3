#!/usr/bin/python3
'''Containing just the place_amenities view thats for the API.'''

from models import storage, storage_t

from flask import jsonify, request

from werkzeug.exceptions import  MethodNotAllowed, NotFound

from api.v1.views import app_views

from models.place import Place

from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST']
)
def handle_places_amenities(place_id=None, amenity_id=None):
    '''
    This function is a method for handler for the placee's endpoint.
    '''
    handllers = {
        'GET': get_place_amenities,
        'DELETE': remove_place_amenity,
        'POST': add_place_amenity
    }
    if request.method in handllers:
        return handllers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handllers.keys()))


def get_place_amenities(place_id=None, amenity_id=None):
    '''Getting the amenities thats of a placee thats with that given id.
    '''
    if place_id:
        placee = storage.get(Place, place_id)
        if placee:
            all_the_amenities = list(map(lambda x: x.to_dict(), placee.amenities))
            return jsonify(all_the_amenities)
    raise NotFound()


def remove_place_amenity(place_id=None, amenity_id=None):
    '''
    Removing an amenitty thats with a particular given id
    from the a place thats with a given id.
    '''
    if place_id and amenity_id:
        placee = storage.get(Place, place_id)
        if not placee:
            raise NotFound()
        amenitty = storage.get(Amenity, amenity_id)
        if not amenitty:
            raise NotFound()
        placee_amenitty_linnk = list(
            filter(lambda x: x.id == amenity_id, placee.amenities)
        )
        if not placee_amenitty_linnk:
            raise NotFound()
        if storage_t == 'db':
            amenitty_placce_linnk = list(
                filter(lambda x: x.id == place_id, amenitty.place_amenities)
            )
            if not amenitty_placce_linnk:
                raise NotFound()
            placee.amenities.remove(amenitty)
            placee.save()
            return jsonify({}), 200
        else:
            amenity_idx = placee.amenity_ids.index(amenity_id)
            placee.amenity_ids.pop(amenity_idx)
            placee.save()
            return jsonify({}), 200
    raise NotFound()


def add_place_amenity(place_id=None, amenity_id=None):
    '''
    Adding an amenity thats with a particular given id thats to a
    place thats with a given id.
    '''
    if place_id and amenity_id:
        placee = storage.get(Place, place_id)
        if not placee:
            raise NotFound()
        amenitty = storage.get(Amenity, amenity_id)
        if not amenitty:
            raise NotFound()
        if storage_t == 'db':
            placee_amenitty_linnk = list(
                filter(lambda x: x.id == amenity_id, placee.amenities)
            )
            amenitty_placce_linnk = list(
                filter(lambda x: x.id == place_id, amenitty.place_amenities)
            )
            if amenitty_placce_linnk and placee_amenitty_linnk:
                ress = amenitty.to_dict()
                del ress['place_amenities']
                return jsonify(ress), 200
            placee.amenities.append(amenitty)
            placee.save()
            ress = amenitty.to_dict()
            del ress['place_amenities']
            return jsonify(ress), 201
        else:
            if amenity_id in placee.amenity_ids:
                return jsonify(amenitty.to_dict()), 200
            placee.amenity_ids.push(amenity_id)
            placee.save()
            return jsonify(amenitty.to_dict()), 201
    raise NotFound()
