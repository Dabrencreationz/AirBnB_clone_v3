#!/usr/bin/python3
"""This returns the status of our api"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response

@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """This returns all our states if successfully connected"""
    return jsonify([x.to_dict() for x in storage.all(State).values()])

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """This returns the given state  who has the givenid if it exist
    or raises a 404"""
    val = storage.get(cls=State, id=state_id)
    if val:
        return jsonify(val.to_dict())
    abort(404)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """This returns the given state  who has the givenid if it exist
    or raises a 404"""
    val = storage.get(cls=State, id=state_id)
    if val:
        storage.delete(val)
        return jsonify({})
    abort(404)

@app_views.route('/states', strict_slashes=False, methods=['DELETE'])
def make_state():
    """This returns the given state  who has the givenid if it exist
    or raises a 404"""
    try:
        data = request.get_json
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)
    if not data.get(name):
        return make_response(jsonify("Missing name"), 400)
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def change_state(state_id):
    """This returns the given state  who has the givenid if it exist
    or raises a 404"""
    try:
        data = request.get_json
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)
    data.pop('id', None)
    data.pop("created_at", None)
    data.pop('updated_at', None)
    state = storage.get(State, state_id)
    for k, v in data.items():
        setattr(state, k, v)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)
