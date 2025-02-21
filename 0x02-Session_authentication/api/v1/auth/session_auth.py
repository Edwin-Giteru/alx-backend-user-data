#!/usr/bin/env python3
from api.v1.auth.auth import Auth
import uuid
from models.user import User

class SessionAuth(Auth):
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        a method that creates a session id for a user id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A method that returns a user id on a session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get('session_id')
    
    def current_user(self, request=None):
        """
        A method that returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None
        return User.get(user_id)
    
    def destroy_session(self, request=None):
        """
        a method that deletes the session/logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id not in request:
            return False
        user_id = User.get(User.id)
        if user_id not in self.user_id_for_session_id(session_id):
            return False
        else:
            del self.user_id_by_session_id[session_id]
        return True