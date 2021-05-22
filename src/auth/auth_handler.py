from __future__ import annotations

import time

import jwt

from src.consts.auth_const import (JWT_ALGORITHM, JWT_EXPIRE_TIME,
                                   JWT_SECRET_KEY)
from src.schemas.token import Token


def sign_jwt(user_id: str) -> Token:
    """created a token string comprising of the payload object"""
    payload = {"user_id": user_id, "expires": time.time() + JWT_EXPIRE_TIME}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return Token(access_token=token)


def decode_jwt(token: str) -> dict:
    """decodes token with the aid of the jwt module
    return decoded_token if the expiry time is valid, otherwise, returned None."""
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    # TODO: zwracany typ None / Dict ?


def hash_password(password: str) -> str:
    """
    Returns hashed password
    :param password: open password
    :return: hashed password
    """
    return password + "notreallyhashed"


# def token_response(token: str):
#     """ helper function for returning generated tokens """
#     return {
#         "access_token": token
#     }
