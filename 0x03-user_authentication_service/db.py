#!/usr/bin/env python3i
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """ a method that save a user and return a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user
    
    def find_user_by(self, **kwargs):
        """
        a method that returns the first row of a table users filtered by the input arguments
        """
        if not kwargs:
            raise InvalidRequestError("no filter arguments provided")
        try:
            return self._session.query(User).filter_by(**kwargs).first()
        except AttributeError:
            raise AttributeError("Invalid attribute in the query")
        except NoResultFound:
            raise NoResultFound("no results for user found")
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        a method that locates a user to update
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound("no user found")
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("invalid attribute")
            setattr(user, key, value)
        self._session.commit()

