from flask import Flask, request, jsonify, make_response, abort
from models.user import User
from os import getenv



app = Flask(__name__)

@app.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or  email == "":
        return jsonify({"error":"email missing"}), 400
    if not password or password == "":
        return jsonify({"error":"password missing"}), 400
    
    users = User.search({"email":email})

    if users is None or len(users) == 0:
        return jsonify({"error":"no user found for this email"}), 404
    user = users[0]

    if not user.is_valid_password(password):
        return  jsonify({"error": "wrong password"})
    from api.v1.app import auth

    
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    session_name = getenv("SESSION_NAME","_my_session_id")
    response.set_cookie(session_name, session_id)
    return response, 200

@app.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def delete_session():
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
