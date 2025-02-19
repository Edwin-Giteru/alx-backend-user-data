import bcrypt

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pwd

def is_valid(hash_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)