#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if getenv('AUTH_TYPE') == 'auth':
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    basic_auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    session_auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    session_exp_auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    session_exp_auth = SessionDBAuth()

@app.before_request
def before_request_func():
    authorized_list = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    
    if auth and auth.require_auth(request.path, authorized_list):
        if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
            abort(401)
     
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    return jsonify({"error": "unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error":"Forbidden"})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(debug=True, host=host, port=port)
