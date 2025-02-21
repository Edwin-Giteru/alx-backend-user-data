from flask import request
from typing import List, TypeVar
import os

class Auth:
    def require_auth(self, path: str, excluded_path: List[str]) ->bool:
        check = path
        if path is None or excluded_path is None or len(excluded_path) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_path or path in excluded_path:
            return False
        return True
    
    def authorization_header(self, request=None) ->str:
        if request is None:
            return None
        if 'Authorization' not in request.keys():
            return None
        return request['Authorization']
    
    def current_user(self, request=None) -> TypeVar("User"):
        """Retrieve a User instance based on the session cookie."""
        return None

    def session_cookie(self, request=None):
        """
        A method that returns a cookie value from a request
        """
        if request is None:
            return None
        os.getenv('SESSION_NAME') == '_my_session_id'
        _my_session_id = request.cookies.get('_my_session_id')
        return _my_session_id