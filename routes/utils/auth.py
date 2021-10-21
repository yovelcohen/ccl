import os
import time
from typing import Dict, Optional

import jwt
from fastapi import HTTPException

JWT_SECRET = os.environ.get('secret', '1')


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 2400
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"))


def decodeJWT(token) -> Optional[dict]:
    if not token:
        return
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return None


def is_authenticated(func):
    """
    decorator that check if a user's token is valid, if not will raise an HTTP 403 exception and break the request
    """

    def _login_user(token):
        decoded = decodeJWT(token=token)
        if decoded:
            return True
        raise HTTPException(status_code=403, detail='token expired')

    def inner(*args, **kwargs):
        _login_user(token=kwargs.pop('accessToken'))
        return func(*args, **kwargs.pop(''))

    return inner
