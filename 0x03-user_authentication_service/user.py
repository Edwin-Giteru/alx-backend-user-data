#!/usr/bin/env python3
"""
an sqlachemy model named User for a database table named users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

