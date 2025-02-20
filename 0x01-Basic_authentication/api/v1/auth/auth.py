from flask import request
from typing import List, TypeVar

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
        return None