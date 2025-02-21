from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None):
       session_id = super().create_session(user_id)

       if not session_id:
           return None
       new_session = UserSession(user_id=user_id, session_id=session_id)
       new_session.save()
       return session_id
    
    def user_id_for_session_id(self, session_id=None):
        if not session_id:
            return None
        session = UserSession.get(session_id=session_id)
        if session:
            return session.user_id
        return None
    
    def destroy_session(self, request=None):
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session  = UserSession.get(session_id=session_id)
        if session:
            session.delete()
            return True
        return False