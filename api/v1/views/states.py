#!/usr/bin/python3
"""This returns the status of our api"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response

@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def work_with_states():
    """This performs various tasks according to
    the request received
    GET: Return all States
    POST: Create a new state"""
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(State).values()])
    elif request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return make_response(jsonify("Not a JSON"), 400)
        if not data.get("name"):
            return make_response(jsonify("Missing name"), 400)
        new_state = State(**data)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def wirk_with_state_id(state_id):
    """This function performs various tasks according to the
    request received
    GET: Return the desired State
    DELETE: Delete the given State
    PUT: Update the given state"""
    val = storage.get(cls=State, id=state_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify(val.to_dict())
    elif request.method == "DELETE":
        storage.delete(val)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception as e:
            return make_response(jsonify("Not a JSON"), 400)
        data.pop('id', None)
        data.pop("created_at", None)
        data.pop('updated_at', None)
        for k, v in data.items():
            setattr(val, k, v)
        #val.save()
        return make_response(jsonify(val.to_dict()), 200)

