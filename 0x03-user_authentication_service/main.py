#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'hiraumaqw@.com'
password = 'todayssf'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

