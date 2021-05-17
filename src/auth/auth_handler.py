from __future__ import annotations

import time

import jwt

from src.consts.auth_const import JWT_ALGORITHM, JWT_EXPIRE_TIME, JWT_SECRET_KEY
from src.schemas.token import Token

# JWT_SECRET = config("secret")
# JWT_ALGORITHM = config("algorithm")

# Every JWT has an expiry date and/or time where it becomes invalid. The jwt module is responsible for encoding and decoding generated token strings. Lastly, the token_response function is a helper function for returning generated tokens.
# def token_response(token: str):
#     return {
#         "access_token": token
#     }


# In the signJWT function, we defined the payload, a dictionary containing the user_id passed into the function, and an expiry time of ten minutes from when it is generated. Next, we created a token string comprising of the payload, the secret, and the algorithm type and then returned it.
def signJWT(user_id: str) -> Token:  # : # Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + JWT_EXPIRE_TIME}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # return token_response(token)
    return Token(access_token=token)


# The decodeJWT function takes the token and decodes it with the aid of the jwt module and then stores it in a decoded_token variable. Next, we returned decoded_token if the expiry time is valid, otherwise, we returned None.
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def hash_password(password: str) -> str:
    return password + "notreallyhashed"
