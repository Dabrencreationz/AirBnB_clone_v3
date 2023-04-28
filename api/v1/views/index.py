#!/usr/bin/python3
"""This returns the status of our api"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """This returns our status if successfully connected"""
    return jsonify({'stauts': "OK"})
