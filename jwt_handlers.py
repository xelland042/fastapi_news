import time
import jwt
from decouple import config
from passlib.context import CryptContext

JWT_SECRET = config('SECRET_KEY')
JWT_ALGORITH = config('ALGORITH')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def token_response(token: str):
    return {
        'access token': token
    }


def signJWT(userID: int):
    payload = {
        'userID': userID,
        'expiry': time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITH)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITH)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
