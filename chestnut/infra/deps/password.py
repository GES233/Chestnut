from bcrypt import gensalt, hashpw, checkpw


def hashpassword(password: str) -> bytes:
    salt = gensalt()
    return hashpw(bytes(password, encoding="utf-8"), salt)


def checkpassword(password: str, hashed_pswd: bytes):
    return checkpw(bytes(password, encoding="utf-8"), hashed_pswd)
