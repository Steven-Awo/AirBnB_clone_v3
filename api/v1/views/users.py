#!/usr/bin/python3
'''Containing just the user views thats for the API.'''

from models import storage

from models.user import User

from flask import jsonify, request

from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])

@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    '''
    Getting the user just with by its given id or by all
    the users.
    '''
    if user_id:
        userr = storage.get(User, user_id)
        if userr:
            objj = userr.to_dict()
            if 'places' in objj:
                del objj['places']
            if 'reviews' in objj:
                del objj['reviews']
            return jsonify(objj)
        raise NotFound()
    all_the_userrs = storage.all(User).values()
    users = []
    for userr in all_the_userrs:
        objj = userr.to_dict()
        if 'places' in objj:
            del objj['places']
        if 'reviews' in objj:
            del objj['reviews']
        users.append(objj)
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    '''
    Removing the user thats with the given id.
    '''
    userr = storage.get(User, user_id)
    if userr:
        storage.delete(userr)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_user():
    '''
    Adding just a new userr.
    '''
    datta = {}
    try:
        datta = request.get_json()
    except Exception:
        datta = None
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in datta:
        raise BadRequest(description='Missing email')
    if 'password' not in datta:
        raise BadRequest(description='Missing password')
    userr = User(**datta)
    userr.save()
    objj = userr.to_dict()
    if 'places' in objj:
        del objj['places']
    if 'reviews' in objj:
        del objj['reviews']
    return jsonify(objj), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''
    Updating the user thats with the given id.
    '''
    x_keys = ('id', 'email', 'created_at', 'updated_at')
    userr = storage.get(User, user_id)
    if userr:
        datta = {}
        try:
            datta = request.get_json()
        except Exception:
            datta = None
        if type(datta) is not dict:
            raise BadRequest(description='Not a JSON')
        for keyy, vallue in datta.items():
            if keyy not in x_keys:
                setattr(userr, keyy, vallue)
        userr.save()
        objj = userr.to_dict()
        if 'places' in objj:
            del objj['places']
        if 'reviews' in objj:
            del objj['reviews']
        return jsonify(objj), 200
    raise NotFound()
