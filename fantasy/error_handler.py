"""
==========================
Fantasy error handle
==========================
"""

from flask import jsonify


def http400(error):
    if hasattr(error, 'data'):
        return jsonify(error.data), 400
    return error, 400


def http422(error):
    if hasattr(error, 'data'):
        return jsonify(error.data), 422
    return error, 422


def http500(error):
    if hasattr(error, 'data'):
        return jsonify(error.data), 500
    return error, 500
