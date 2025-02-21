from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, Tuple
from models.user import User 

class BasicAuth(Auth):
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        
        "A method that returns Base64 part of an Authorization header"

        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:

        "A method that returns the decoded value of Base64 string"

        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decode_bytes.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        
        "A method taht returns the user email and password from Base64 decoded value"

        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str) or ":" not in decoded_base64_authorization_header:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password
        
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):

        "a method that returns User instance based on his email and password"
        
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
         
        users = User.search({"email": user_email})

        if not users or len(users) == 0:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
    
    def current_user(self, request=None) -> TypeVar('User'):

        "A method that Overloads Auth and retrieves User instance for a request"

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        encoded = self.extract_base64_authorization_header(auth_header)

        if encoded is None:
            return  None
        
        decoded = self.decode_base64_authorization_header(encoded)
        
        if decoded is None:
            return None
        
        email, password = self.extract_user_credentials(decoded)
        if email is None or password  is None:
            return None
        
        user = self.user_object_from_credentials(email, password)
        
        return user
