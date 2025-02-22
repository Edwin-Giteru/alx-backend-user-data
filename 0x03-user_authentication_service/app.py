#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, make_response, url_for, redirect
from auth import Auth
Auth = Auth()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users():
    email = request.form.get("email")
    password  = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    try:
       new_user =  Auth.register_user(email, password)
       return jsonify({"email": new_user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not Auth.valid_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged_in"}))
    response.set_cookie("session_id", session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect("/")
    abort(403)

@app.route('/profile', methods=['GET'])
def profile():
    """responds with the user profile """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)
        
@app.route('reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form.get("email")
    try:
        reset_token = Auth.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})

@app.route("/reset_password", methods=['PUT'])
def update_password():
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        Auth.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password_updated"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

