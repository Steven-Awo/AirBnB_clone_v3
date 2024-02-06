#!/usr/bin/python3
'''Containing just the places_reviews views thats for the API.'''

from models import storage

from models.userr import User

from flask import jsonify, request

from werkzeug.exceptions import  MethodNotAllowed, NotFound, BadRequest

from api.v1.views import app_views

from models.place import Place

from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])

@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews(place_id=None, review_id=None):
    '''
    This function is a method for handler for the reviewws's endpoint.
    '''
    handllers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in handllers:
        return handllers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handllers.keys()))


def get_reviews(place_id=None, review_id=None):
    '''
    Getting the reviewws just with by its given id or by all
    the reviewss.
    '''
    if place_id:
        placee = storage.get(Place, place_id)
        if placee:
            reviewws = []
            for revieww in placee.reviewws:
                reviewws.append(revieww.to_dict())
            return jsonify(reviewws)
    elif review_id:
        revieww = storage.get(Review, review_id)
        if revieww:
            return jsonify(revieww.to_dict())
    raise NotFound()


def remove_review(place_id=None, review_id=None):
    '''Removing the revieww thats with the given id.
    '''
    revieww = storage.get(Review, review_id)
    if revieww:
        storage.delete(revieww)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_review(place_id=None, review_id=None):
    '''
    Adding just a new revieww.
    '''
    placee = storage.get(Place, place_id)
    if not placee:
        raise NotFound()
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in datta:
        raise BadRequest(description='Missing user_id')
    userr = storage.get(User, datta['user_id'])
    if not userr:
        raise NotFound()
    if 'text' not in datta:
        raise BadRequest(description='Missing text')
    datta['place_id'] = place_id
    newer_revieww = Review(**datta)
    newer_revieww.save()
    return jsonify(newer_revieww.to_dict()), 201


def update_review(place_id=None, review_id=None):
    '''
    Updating the review thats with the given id.
    '''
    x_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        revieww = storage.get(Review, review_id)
        if revieww:
            datta = request.get_json()
            if type(datta) is not dict:
                raise BadRequest(description='Not a JSON')
            for keyy, valuee in datta.items():
                if keyy not in x_keys:
                    setattr(revieww, keyy, valuee)
            revieww.save()
            return jsonify(revieww.to_dict()), 200
    raise NotFound()
