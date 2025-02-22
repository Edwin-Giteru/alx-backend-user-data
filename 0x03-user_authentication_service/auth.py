#!/usr/bin/env python3
"""
define a _hash_password method that returna a salted hash of the input password
"""
import uuid
import bcrypt
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

from db import DB

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        """
        a method that checks an email with a password exists and hash the password
        """
        try:
            user = self._db.find_user_by(email=email)
            print("User already exists:", user)  # Debugging
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            print("No existing user, proceeding to register...")  # Debugging

        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        print("New user registered:", new_user)  # Debugging
        return new_user
    
    def valid_login(self, email: str, password: str) -> bool:
        """
        a method that should locate if an email exists and check if passwords matches 
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))


    def _generate_uuid(self) -> str:
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        a method should find the user corresponding to the email and return session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
    
    def get_user_from_session_id(self, session_id: str) -> User:
        """
        checks if a user has a session
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id = session_id)
        except NoResultFound:
            return None
        return user
    
    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding users sessionid to none
        """
        self._db.update_user(user_id, session_id=None)
    
    def get_reset_password_token(self, email: str) -> str:
        """
        a method updates a token to an existing user
        """
        try:
             user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
    
    def update_password(self, reset_token: str, password: str) -> None:
        """
        a method that updates password by finding the user with a reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, password=_hash_password(password), reset_token=None)
