#!/usr/bin/python3
'''Containing just the amenities views thats for the API.'''

from models import storage

from models.state import State

from flask import jsonify, request

from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

from api.v1.views import app_views


ALLOWED_METHODS = ['GET', 'POST', 'DELETE', 'PUT']
'''Methods that are allowed just for the amenitie's endpoint.'''


@app_views.route('/states', methods=ALLOWED_METHODS)

@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    '''The method handler for the states endpoint.
    '''
    handlers = {
        'GET': get_states,
        'DELETE': remove_state,
        'POST': add_state,
        'PUT': update_state,
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_states(state_id=None):
    '''
    Getting the states just with by its given id or by all
    the states.
    '''
    all_the_states = storage.all(State).values()
    if state_id:
        ress = list(filter(lambda y: y.id == state_id, all_the_states))
        if ress:
            return jsonify(ress[0].to_dict())
        raise NotFound()
    all_the_states = list(map(lambda y: y.to_dict(), all_the_states))
    return jsonify(all_the_states)


def remove_state(state_id=None):
    '''
    Removing the state thats with the given id.
    '''
    all_the_states = storage.all(State).values()
    ress = list(filter(lambda y: y.id == state_id, all_the_states))
    if ress:
        storage.delete(ress[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    '''
    Adding just a new state.
    '''
    datta = request.get_json()
    if type(datta) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in datta:
        raise BadRequest(description='Missing name')
    neww_statee = State(**datta)
    neww_statee.save()
    return jsonify(neww_statee.to_dict()), 201


def update_state(state_id=None):
    '''
    Updating the state thats with the given id.
    '''
    x_keys = ('id', 'created_at', 'updated_at')
    all_the_states = storage.all(State).values()
    ress = list(filter(lambda y: y.id == state_id, all_the_states))
    if ress:
        datta = request.get_json()
        if type(datta) is not dict:
            raise BadRequest(description='Not a JSON')
        older_statee = ress[0]
        for key, value in datta.items():
            if key not in x_keys:
                setattr(older_statee, key, value)
        older_statee.save()
        return jsonify(older_statee.to_dict()), 200
    raise NotFound()
