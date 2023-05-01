#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_city_places(city_id):
    """This performs various tasks according to
    the request received
    GET: Return all places in a city
    POST: Create/add a new place"""
    val = storage.get(cls=City, id=city_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in val.places])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_place_id(place_id):
    """This function performs various tasks according to the
    request received
    GET: Return the desired place
    DELETE: Delete the given place
    PUT: Update the given place"""
    val = storage.get(cls=Place, id=place_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify(val.to_dict())
    elif request.method == "DELETE":
        val.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        for k, v in data.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(val, k, v)
        val.save()
        return make_response(jsonify(val.to_dict()), 200)


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def place_search():
    data = request.get_json()
    if data is None:
        return make_response(jsonify("Not a JSON"), 400)
    if data and len(data):
        sta_s = data.get(states, None)
        ci_s = data.get(cities, None)
        ame = data.get(amenities, None)
    if ((not data) or
            (not len(data)) or
            (sta_s is None and ci_s is None and ame is None)):
        return jsonify([x.to_dict() for x in storage.all(Places).values()])
    result = []
    amen = []
    if sta_s:
        for id_ in sta_s:
            val = storage.get(State, id_)
            if val:
                for city in val.cities:
                    for place in city.places:
                        result.append(place)
    if ci_s:
        for id_ in ci_s:
            val = storage.get(City, id_)
            if val:
                for place in val.places:
                    if place not in result:
                        result.append(place)
    if ame:
        for id_ in ame:
            val = storage.get(Amenity, id_)
            if val:
                amen.append(val)
    if amen:
        result = [x for x in result
                  if all(mem in place.amenities for mem in amen)]
    return jsonify([x.to_dict() for x in result])
